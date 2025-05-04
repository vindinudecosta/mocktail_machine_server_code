from flask import Flask, request, render_template, jsonify,Response
import os
import ctranslate2
import threading
import tensorflow as tf
import json
import random
import pickle
import numpy as np
from transformers import WhisperProcessor
import io
import soundfile as sf  # For in-memory audio processing
import time
import logging
from flask_cors import CORS
app = Flask(__name__)
import queue

CORS(app)  # Enable CORS
# Set up logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Log CTranslate2 version
logger.info(f"CTranslate2 version: {ctranslate2.__version__}")

# Load resources once at startup
processor = WhisperProcessor.from_pretrained("openai/whisper-small")
ct_model_path = "D:/Documents/OUSL_mechatronics_level5_resources/design project resourses/server side/whisper-small-ct2"
try:
    whisper_model = ctranslate2.models.Whisper(ct_model_path, device="cpu", intra_threads=6)  # Adjust based on CPU cores
    logger.info("Whisper model loaded successfully with 6 intra-threads")
except Exception as e:
    logger.error(f"Failed to load Whisper model: {str(e)}")
    raise

intent_model = tf.keras.models.load_model("intent_recognition_model_V1.h5")

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open('intents.json', 'r') as f:
    data = json.load(f)

response_for_intent = {intent['intent']: intent['responses'] for intent in data['intents']}

# Global variables for transcription
audio_chunks = []
transcription_result = None
transcription_ready = threading.Event()
transcribe_lock = threading.Lock()

@app.route('/audio', methods=['POST'])
def process_audio():
    global audio_chunks, transcription_result, transcription_ready

    if not transcribe_lock.acquire(blocking=False):
        logger.warning("Server is busy")
        return "Server is busy. Try again later.", 503

    try:
        logger.debug(f"Received chunk, total chunks: {len(audio_chunks) + 1}")
        audio_chunks.append(request.data)

        if len(audio_chunks) >= 2:
            # Combine chunks in-memory
            raw_audio_data = b''.join(audio_chunks)
            logger.debug(f"Raw audio size: {len(raw_audio_data)} bytes")

            try:
                logger.debug("Processing raw audio in-memory")
                # Convert raw PCM to NumPy array
                audio_array = np.frombuffer(raw_audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                
                # Ensure mono and 16kHz (Whisper expects this)
                if len(audio_array.shape) > 1:  # If stereo, take first channel
                    audio_array = audio_array[:, 0]
                
                # Pad or trim to 30s (480,000 samples at 16kHz)
                target_length = 480000
                if len(audio_array) < target_length:
                    audio_array = np.pad(audio_array, (0, target_length - len(audio_array)), mode='constant')
                else:
                    audio_array = audio_array[:target_length]
                logger.debug(f"Audio shape: {audio_array.shape}")

                # Extract features
                features = processor(audio_array, sampling_rate=16000, return_tensors="np").input_features
                logger.debug(f"Features shape: {features.shape}")

                # Convert to CTranslate2 StorageView
                features_storage = ctranslate2.StorageView.from_array(features)
                logger.debug(f"Features storage type: {type(features_storage)}")

                # Perform inference with CTranslate2 Whisper
                result = whisper_model.generate(
                    features_storage,
                    [[50258, 50259, 50359]],  # Hardcoded SOT sequence for English
                    beam_size=1  # Reduce beam search for speed
                )
                transcription_result = processor.tokenizer.decode(result[0].sequences_ids[0])
                transcription_ready.set()
                audio_chunks.clear()
                logger.info(f"Transcription completed successfully: {transcription_result}")

            except Exception as e:
                logger.error(f"Error during processing: {str(e)}")
                return f"Error during processing: {str(e)}", 500
            finally:
                # No files to remove since we’re in-memory
                pass

            return "Transcription completed.", 200
        else:
            return "Chunk received. Waiting for more chunks...", 200
    finally:
        transcribe_lock.release()
        logger.debug("Released transcription lock")

@app.route('/result', methods=['GET'])
def get_transcription_result():
    if not transcription_ready.wait(timeout=10):
        logger.warning("Transcription not ready within timeout")
        return "Transcription not available yet. Please try again.", 404

    transcription_ready.clear()
    return transcription_result, 200

@app.route('/intent', methods=['POST'])
def intent_recognition():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "TextUnidentified"}), 400

    try:
        sequence = tokenizer.texts_to_sequences([text])
        padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, padding='pre', maxlen=5)
        intent_pred = intent_model.predict(padded_sequence, verbose=0)
        intent_class = intent_pred.argmax(axis=1)[0]
        intent = list(response_for_intent.keys())[intent_class]
        response = random.choice(response_for_intent[intent])
        return jsonify({"intent": intent, "response": response})
    except Exception as e:
        return jsonify({"error": f"Intent recognition error: {str(e)}"}), 500
    

# Global event queue
event_queue = queue.Queue()
clients = []

@app.route('/status-stream')
def status_stream():
    def event_stream():
        try:
            while True:
                try:
                    # Get message from queue with timeout
                    message = event_queue.get(timeout=30)  # 30 second timeout
                    # Properly formatted SSE message
                    yield f"event: status_update\ndata: {json.dumps(message)}\n\n"
                except queue.Empty:
                    # Send keepalive comment
                    yield ":keepalive\n\n"
                    
        except GeneratorExit:
            logger.info("Client disconnected from SSE stream")
        except Exception as e:
            logger.error(f"SSE stream error: {str(e)}")

    response = Response(event_stream(), mimetype="text/event-stream")
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    return response
@app.route('/update-status', methods=['POST'])
def update_status():
    logger.debug(f"Received POST /update-status: {request.json}")
    try:
        data = request.json
        drink_name = data.get('drink')
        message = data.get('message')
        duration = data.get('duration', 1000)

        if not drink_name or not message:
            logger.error("Invalid status update: missing drink or message")
            return jsonify({"error": "Invalid status update"}), 400

        # Create status update message
        status_update = {
            "type": "status_update",
            "drink": drink_name,
            "message": message,
            "duration": duration,
            "timestamp": time.time()
        }
        

        # Add to event queue for SSE
        event_queue.put(status_update)

        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Error updating status: {str(e)}")
        return jsonify({"error": f"Error updating status: {str(e)}"}), 500
   

@app.route('/')
def index():
    return render_template('index_2.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False)