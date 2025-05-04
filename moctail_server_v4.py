from flask import Flask, request, render_template, jsonify
import subprocess
import os
import whisper
import threading
import torch
import tensorflow as tf
import json
import random
import pickle

app = Flask(__name__)
#best version
# Load resources once at startup
device = torch.device("cpu")
whisper_model = whisper.load_model("small").to(device)
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
        return "Server is busy. Try again later.", 503

    try:
        audio_chunks.append(request.data)

        # Process when enough chunks are received
        if len(audio_chunks) >= 3:
            audio_file = "audio.raw"
            with open(audio_file, "wb") as f:
                f.writelines(audio_chunks)

            converted_audio = "audio.wav"
            try:
                subprocess.run(
                    ["ffmpeg", "-y", "-f", "s16le", "-ar", "16000", "-ac", "1", "-i", audio_file, converted_audio],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

                result = whisper_model.transcribe(converted_audio, fp16=False, language="en")
                transcription_result = result['text']
                transcription_ready.set()
                audio_chunks.clear()

            except subprocess.TimeoutExpired:
                return "Audio conversion timeout.", 500
            except Exception as e:
                return f"Error during processing: {str(e)}", 500
            finally:
                os.remove(audio_file)
                os.remove(converted_audio)

            return "Transcription completed.", 200
        else:
            return "Chunk received. Waiting for more chunks...", 200
    finally:
        transcribe_lock.release()

@app.route('/result', methods=['GET'])
def get_transcription_result():
    if not transcription_ready.wait(timeout=30):
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
