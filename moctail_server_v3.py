from flask import Flask, request, jsonify
import subprocess
import os
import whisper
import threading
import torch  # Ensure PyTorch is imported
import tensorflow as tf
import json
import random
import pickle

app = Flask(__name__)

# Force PyTorch to use the CPU
device = torch.device("cpu")

# Load the Whisper model and ensure it runs on the CPU
whisper_model = whisper.load_model("medium").to(device)

# Load the intent recognition model
intent_model = tf.keras.models.load_model("intent_recognition_model_V1.h5")

# Load the tokenizer used during training
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load intents from the JSON file
with open('intents.json', 'r') as f:
    data = json.load(f)

# Create a dictionary for responses by intent
response_for_intent = {}
for intent in data['intents']:
    response_for_intent[intent['intent']] = intent['responses']

# Global variables for managing transcription
audio_chunks = []
transcription_result = None
transcription_ready = threading.Event()  # Event to signal when transcription is ready
transcribe_lock = threading.Lock()  # Lock to handle concurrent requests

@app.route('/audio', methods=['POST'])
def process_audio():
    global audio_chunks, transcription_result, transcription_ready

    # Check if the server is busy
    if not transcribe_lock.acquire(blocking=False):
        return "Server is busy. Try again later.", 503

    try:
        # Append incoming chunk to the buffer
        audio_chunks.append(request.data)

        # If 5 chunks are accumulated, process them
        if len(audio_chunks) == 3:
            audio_file = "audio.raw"
            with open(audio_file, "wb") as f:
                for chunk in audio_chunks:
                    f.write(chunk)

            # Convert the raw audio to WAV using FFmpeg
            converted_audio = "audio.wav"
            try:
                subprocess.run(
                    ["ffmpeg", "-y", "-f", "s16le", "-ar", "16000", "-ac", "1", "-i", audio_file, converted_audio],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=1,
                )
            except Exception as e:
                return f"Audio conversion error: {str(e)}", 500

            # Transcribe the WAV file using Whisper
            try:
                result = whisper_model.transcribe(converted_audio, fp16=False, language="en")
                transcription_result = result['text']
                transcription_ready.set()  # Signal that transcription is ready
                audio_chunks = []  # Clear buffer
            except Exception as e:
                return f"Transcription error: {str(e)}", 500
            finally:
                # Clean up temporary files
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                if os.path.exists(converted_audio):
                    os.remove(converted_audio)

            return "Transcription completed.", 200
        else:
            return "Chunk received. Waiting for more chunks...", 200
    finally:
        # Release the lock
        transcribe_lock.release()

@app.route('/result', methods=['GET'])
def get_transcription_result():
    global transcription_result

    # Wait for the transcription to complete (with a timeout of 30 seconds)
    if not transcription_ready.wait(timeout=30):
        return "Transcription not available yet. Please try again.", 404

    transcription_ready.clear()  # Reset the event for the next transcription
    return transcription_result, 200

@app.route('/intent', methods=['POST'])
def intent_recognition():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "TextUnidentified"}), 400

    try:
        # Convert the input text to a sequence using the loaded tokenizer
        sequence = tokenizer.texts_to_sequences([text])
        
        # Pad the sequence to match the input shape expected by the model (length 5)
        padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, padding='pre', maxlen=5)

        # Predict intent
        intent_pred = intent_model.predict(padded_sequence)
        intent_class = intent_pred.argmax(axis=1)[0]

        # Get response for the predicted intent
        intent = list(response_for_intent.keys())[intent_class]
        response = random.choice(response_for_intent[intent])

        return jsonify({"intent": intent, "response": response})
    except Exception as e:
        return jsonify({"error": f"Intent recognition error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False)
