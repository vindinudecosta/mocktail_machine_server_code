# from flask import Flask, request, render_template, jsonify
# import subprocess
# import os
# import ctranslate2
# import threading
# import tensorflow as tf
# import json
# import random
# import pickle
# import numpy as np
# from transformers import WhisperProcessor
# import whisper  # Explicitly import openai-whisper

# app = Flask(__name__)

# # Set up logging
# import logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# # Log CTranslate2 version
# logger.info(f"CTranslate2 version: {ctranslate2.__version__}")

# # Load resources once at startup
# processor = WhisperProcessor.from_pretrained("openai/whisper-small")  # For feature extraction and decoding
# ct_model_path = "D:/Documents/OUSL_mechatronics_level5_resources/design project resourses/server side/whisper-small-ct2"
# try:
#     whisper_model = ctranslate2.models.Whisper(ct_model_path)
#     logger.info("Whisper model loaded successfully")
# except Exception as e:
#     logger.error(f"Failed to load Whisper model: {str(e)}")
#     raise

# intent_model = tf.keras.models.load_model("intent_recognition_model_V1.h5")

# with open('tokenizer.pickle', 'rb') as handle:
#     tokenizer = pickle.load(handle)

# with open('intents.json', 'r') as f:
#     data = json.load(f)

# response_for_intent = {intent['intent']: intent['responses'] for intent in data['intents']}

# # Global variables for transcription
# audio_chunks = []
# transcription_result = None
# transcription_ready = threading.Event()
# transcribe_lock = threading.Lock()

# @app.route('/audio', methods=['POST'])
# def process_audio():
#     global audio_chunks, transcription_result, transcription_ready

#     if not transcribe_lock.acquire(blocking=False):
#         logger.warning("Server is busy")
#         return "Server is busy. Try again later.", 503

#     try:
#         logger.debug(f"Received chunk, total chunks: {len(audio_chunks) + 1}")
#         audio_chunks.append(request.data)

#         # Process when enough chunks are received
#         if len(audio_chunks) >= 1:
#             audio_file = "audio.raw"
#             with open(audio_file, "wb") as f:
#                 f.writelines(audio_chunks)

#             converted_audio = "audio.wav"
#             try:
#                 logger.debug("Converting raw audio to WAV")
#                 subprocess.run(
#                     ["ffmpeg", "-y", "-f", "s16le", "-ar", "16000", "-ac", "1", "-i", audio_file, converted_audio],
#                     check=True,
#                     stdout=subprocess.DEVNULL,
#                     stderr=subprocess.DEVNULL,
#                 )

#                 logger.debug("Loading and transcribing audio with Whisper")
#                 # Load WAV audio using openai-whisper
#                 audio = whisper.load_audio(converted_audio)
#                 audio = whisper.pad_or_trim(audio)
#                 logger.debug(f"Audio shape: {audio.shape}")
                
#                 # Extract features
#                 features = processor(audio, sampling_rate=16000, return_tensors="np").input_features
#                 logger.debug(f"Features shape: {features.shape}")
                
#                 # Convert NumPy array to CTranslate2 StorageView (keep 3D)
#                 features_storage = ctranslate2.StorageView.from_array(features)
#                 logger.debug(f"Features storage type: {type(features_storage)}")
                
#                 # Perform inference with CTranslate2 Whisper
#                 result = whisper_model.generate(
#                     features_storage,
#                     [[50258, 50259, 50359]]  # Hardcoded SOT sequence for English
#                 )
#                 # Decode tokens using WhisperProcessor's tokenizer
#                 transcription_result = processor.tokenizer.decode(result[0].sequences_ids[0])
#                 transcription_ready.set()
#                 audio_chunks.clear()
#                 logger.info(f"Transcription completed successfully: {transcription_result}")

#             except subprocess.TimeoutExpired:
#                 logger.error("FFmpeg conversion timed out")
#                 return "Audio conversion timeout.", 500
#             except Exception as e:
#                 logger.error(f"Error during processing: {str(e)}")
#                 return f"Error during processing: {str(e)}", 500
#             finally:
#                 # Ensure files are removed even on failure
#                 for file in [audio_file, converted_audio]:
#                     if os.path.exists(file):
#                         try:
#                             os.remove(file)
#                             logger.debug(f"Removed {file}")
#                         except Exception as e:
#                             logger.warning(f"Failed to remove {file}: {str(e)}")

#             return "Transcription completed.", 200
#         else:
#             return "Chunk received. Waiting for more chunks...", 200
#     finally:
#         transcribe_lock.release()
#         logger.debug("Released transcription lock")

# @app.route('/result', methods=['GET'])
# def get_transcription_result():
#     if not transcription_ready.wait(timeout=30):
#         logger.warning("Transcription not ready within timeout")
#         return "Transcription not available yet. Please try again.", 404

#     transcription_ready.clear()
#     return transcription_result, 200

# @app.route('/intent', methods=['POST'])
# def intent_recognition():
#     data = request.json
#     text = data.get('text', '')

#     if not text:
#         return jsonify({"error": "TextUnidentified"}), 400

#     try:
#         sequence = tokenizer.texts_to_sequences([text])
#         padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, padding='pre', maxlen=5)

#         intent_pred = intent_model.predict(padded_sequence, verbose=0)
#         intent_class = intent_pred.argmax(axis=1)[0]

#         intent = list(response_for_intent.keys())[intent_class]
#         response = random.choice(response_for_intent[intent])

#         return jsonify({"intent": intent, "response": response})
#     except Exception as e:
#         return jsonify({"error": f"Intent recognition error: {str(e)}"}), 500
    
# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False)




# from flask import Flask, request, render_template, jsonify
# import subprocess
# import os
# import ctranslate2
# import threading
# import tensorflow as tf
# import json
# import random
# import pickle
# import numpy as np
# from transformers import WhisperProcessor
# import whisper  # Explicitly import openai-whisper

# app = Flask(__name__)

# # Set up logging
# import logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# # Log CTranslate2 version
# logger.info(f"CTranslate2 version: {ctranslate2.__version__}")

# # Load resources once at startup
# processor = WhisperProcessor.from_pretrained("openai/whisper-medium")  # Updated to medium
# ct_model_path = "D:/Documents/OUSL_mechatronics_level5_resources/design project resourses/server side/whisper-medium-ct2"  # Updated path
# try:
#     whisper_model = ctranslate2.models.Whisper(ct_model_path)
#     logger.info("Whisper model loaded successfully")
# except Exception as e:
#     logger.error(f"Failed to load Whisper model: {str(e)}")
#     raise

# intent_model = tf.keras.models.load_model("intent_recognition_model_V1.h5")

# with open('tokenizer.pickle', 'rb') as handle:
#     tokenizer = pickle.load(handle)

# with open('intents.json', 'r') as f:
#     data = json.load(f)

# response_for_intent = {intent['intent']: intent['responses'] for intent in data['intents']}

# # Global variables for transcription
# audio_chunks = []
# transcription_result = None
# transcription_ready = threading.Event()
# transcribe_lock = threading.Lock()

# @app.route('/audio', methods=['POST'])
# def process_audio():
#     global audio_chunks, transcription_result, transcription_ready

#     if not transcribe_lock.acquire(blocking=False):
#         logger.warning("Server is busy")
#         return "Server is busy. Try again later.", 503

#     try:
#         logger.debug(f"Received chunk, total chunks: {len(audio_chunks) + 1}")
#         audio_chunks.append(request.data)

#         # Process when enough chunks are received
#         if len(audio_chunks) >= 1:
#             audio_file = "audio.raw"
#             with open(audio_file, "wb") as f:
#                 f.writelines(audio_chunks)

#             converted_audio = "audio.wav"
#             try:
#                 logger.debug("Converting raw audio to WAV")
#                 subprocess.run(
#                     ["ffmpeg", "-y", "-f", "s16le", "-ar", "16000", "-ac", "1", "-i", audio_file, converted_audio],
#                     check=True,
#                     stdout=subprocess.DEVNULL,
#                     stderr=subprocess.DEVNULL,
#                 )

#                 logger.debug("Loading and transcribing audio with Whisper")
#                 # Load WAV audio using openai-whisper
#                 audio = whisper.load_audio(converted_audio)
#                 audio = whisper.pad_or_trim(audio)
#                 logger.debug(f"Audio shape: {audio.shape}")
                
#                 # Extract features
#                 features = processor(audio, sampling_rate=16000, return_tensors="np").input_features
#                 logger.debug(f"Features shape: {features.shape}")
                
#                 # Convert NumPy array to CTranslate2 StorageView (keep 3D)
#                 features_storage = ctranslate2.StorageView.from_array(features)
#                 logger.debug(f"Features storage type: {type(features_storage)}")
                
#                 # Perform inference with CTranslate2 Whisper
#                 result = whisper_model.generate(
#                     features_storage,
#                     [[50258, 50259, 50359]]  # Hardcoded SOT sequence for English
#                 )
#                 # Decode tokens using WhisperProcessor's tokenizer
#                 transcription_result = processor.tokenizer.decode(result[0].sequences_ids[0])
#                 transcription_ready.set()
#                 audio_chunks.clear()
#                 logger.info(f"Transcription completed successfully: {transcription_result}")

#             except subprocess.TimeoutExpired:
#                 logger.error("FFmpeg conversion timed out")
#                 return "Audio conversion timeout.", 500
#             except Exception as e:
#                 logger.error(f"Error during processing: {str(e)}")
#                 return f"Error during processing: {str(e)}", 500
#             finally:
#                 # Ensure files are removed even on failure
#                 for file in [audio_file, converted_audio]:
#                     if os.path.exists(file):
#                         try:
#                             os.remove(file)
#                             logger.debug(f"Removed {file}")
#                         except Exception as e:
#                             logger.warning(f"Failed to remove {file}: {str(e)}")

#             return "Transcription completed.", 200
#         else:
#             return "Chunk received. Waiting for more chunks...", 200
#     finally:
#         transcribe_lock.release()
#         logger.debug("Released transcription lock")

# @app.route('/result', methods=['GET'])
# def get_transcription_result():
#     if not transcription_ready.wait(timeout=30):
#         logger.warning("Transcription not ready within timeout")
#         return "Transcription not available yet. Please try again.", 404

#     transcription_ready.clear()
#     return transcription_result, 200

# @app.route('/intent', methods=['POST'])
# def intent_recognition():
#     data = request.json
#     text = data.get('text', '')

#     if not text:
#         return jsonify({"error": "TextUnidentified"}), 400

#     try:
#         sequence = tokenizer.texts_to_sequences([text])
#         padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, padding='pre', maxlen=5)

#         intent_pred = intent_model.predict(padded_sequence, verbose=0)
#         intent_class = intent_pred.argmax(axis=1)[0]

#         intent = list(response_for_intent.keys())[intent_class]
#         response = random.choice(response_for_intent[intent])

#         return jsonify({"intent": intent, "response": response})
#     except Exception as e:
#         return jsonify({"error": f"Intent recognition error: {str(e)}"}), 500
    
# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False)


from flask import Flask, request, render_template, jsonify
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

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False)