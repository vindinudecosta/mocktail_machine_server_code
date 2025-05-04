# from flask import Flask, request, jsonify
# import numpy as np
# import wave
# import os
# import whisper

# app = Flask(__name__)

# # Load Whisper model
# try:
#     model = whisper.load_model("base")
#     print("Whisper model loaded successfully.")
# except Exception as e:
#     print(f"Error loading Whisper model: {e}")
#     model = None

# # Directory to save received audio chunks
# AUDIO_DIR = os.path.join(os.getcwd(), "audio_chunks")
# os.makedirs(AUDIO_DIR, exist_ok=True)
# print(f"Audio chunks will be saved to: {AUDIO_DIR}")


# @app.route('/transcribe', methods=['POST'])
# def transcribe_audio():
#     try:
#         # Receive raw audio data
#         audio_data = request.data
#         print(f"Received data size: {len(audio_data)} bytes")
        
#         if not audio_data:
#             return jsonify({"error": "No data received"}), 400
        
#         # Convert raw audio data to numpy array
#         audio_array = np.frombuffer(audio_data, dtype=np.uint16)
#         print(f"Audio array (first 10 samples): {audio_array[:10]}")
        
#         # Scale the audio data to 16-bit PCM range
#         audio_array = (audio_array - 2048) * 16

#         # Save the audio data as a WAV file
#         chunk_path = os.path.join(AUDIO_DIR, "received_chunk.wav")
#         print(f"Saving chunk to: {chunk_path}")

#         with wave.open(chunk_path, "wb") as wav_file:
#             wav_file.setnchannels(1)  # Mono audio
#             wav_file.setsampwidth(2)  # 16-bit PCM
#             wav_file.setframerate(16000)  # 16 kHz sampling rate
#             wav_file.writeframes(audio_array.tobytes())

#         # Perform transcription using Whisper
#         if model:
#             print("Starting transcription...")
#             result = model.transcribe(chunk_path)
#             transcription = result.get("text", "Transcription failed")
#             print(f"Transcription result: {transcription}")
#         else:
#             return jsonify({"error": "Whisper model not loaded"}), 500

#         # Return the transcription
#         return jsonify({"status": "success", "transcription": transcription})

#     except Exception as e:
#         # Log the exception and return an error response
#         print(f"Error during processing: {e}")
#         return jsonify({"error": str(e)}), 500


# if __name__ == '__main__':
#     # Start the Flask server
#     app.run(host='0.0.0.0', port=5000, debug=True)



# from flask import Flask, request
# import subprocess
# import os
# import whisper

# app = Flask(__name__)

# model = whisper.load_model("base")

# @app.route('/audio', methods=['POST'])
# def process_audio():
#     # Save received audio
#     audio_file = "audio.raw"
#     with open(audio_file, "wb") as f:
#         f.write(request.data)
    
#     # Convert to Whisper-compatible format using FFmpeg
#     converted_audio = "audio.wav"
#     try:
#         subprocess.run([
#             "ffmpeg", "-y", "-f", "s16le", "-ar", "16000", "-ac", "1", "-i", audio_file, converted_audio
#         ], check=True)
#     except subprocess.CalledProcessError as e:
#         return f"FFmpeg error: {e.stderr.decode()}", 500
    
#     # Transcribe using Whisper
#     try:
#         result = model.transcribe(converted_audio, fp16=False)
#         return result['text'], 200
#     except Exception as e:
#         return f"Whisper error: {str(e)}", 500
#     finally:
#         # Clean up files
#         if os.path.exists(audio_file):
#             os.remove(audio_file)
#         if os.path.exists(converted_audio):
#             os.remove(converted_audio)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)


# from flask import Flask, request
# import subprocess
# import os
# import whisper
# import io

# app = Flask(__name__)

# # Load the Whisper model
# model = whisper.load_model("small")


# # Buffer to store chunks before conversion
# audio_chunks = []
# @app.route('/audio', methods=['POST'])
# def process_audio():
#     global audio_chunks
    
#     # Append incoming chunk to the buffer
#     audio_chunks.append(request.data)
    
#     # If 5 chunks are accumulated, process them
#     if len(audio_chunks) == 5:
#         # Save accumulated audio as raw data to a file
#         audio_file = "audio.raw"
#         with open(audio_file, "wb") as f:
#             for chunk in audio_chunks:
#                 f.write(chunk)
        
#         # Convert the raw audio to WAV using FFmpeg
#         converted_audio = "audio.wav"
#         try:
#             result = subprocess.run([
#                 "ffmpeg", "-y", "-f", "s16le", "-ar", "16000", "-ac", "1", "-i", audio_file, converted_audio
#             ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
#             print(f"FFmpeg output: {result.stdout.decode()}")
#             print(f"FFmpeg error (if any): {result.stderr.decode()}")
#         except subprocess.CalledProcessError as e:
#             return f"FFmpeg error: {e.stderr.decode()}", 500
#         except subprocess.TimeoutExpired:
#             return "FFmpeg process timed out", 500
        
#         # Transcribe the WAV file to text using Whisper
#         try:
#             result = model.transcribe(converted_audio, fp16=False, language="en")
#             transcription = result['text']
            
#             # Clear the buffer after processing
#             audio_chunks = []
            
#             return transcription, 200  # Return the transcription as the response
#         except Exception as e:
#             return f"Whisper error: {str(e)}", 500
#         finally:
#             # Clean up the files after processing
#             if os.path.exists(audio_file):
#                 os.remove(audio_file)
#             if os.path.exists(converted_audio):
#                 os.remove(converted_audio)
    
#     return "Waiting for more chunks...", 200


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)


from flask import Flask, request
import subprocess
import os
import whisper
import threading

app = Flask(__name__)

# Load the Whisper model
model = whisper.load_model("small")

# Buffer to store chunks before conversion
audio_chunks = []
transcribe_lock = threading.Lock()
transcription_result = None  # Store the latest transcription result

@app.route('/audio', methods=['POST'])
def process_audio():
    global audio_chunks, transcription_result

    # Check if the server is busy
    if not transcribe_lock.acquire(blocking=False):
        return "Server is busy. Try again later.", 503

    try:
        # Append incoming chunk to the buffer
        audio_chunks.append(request.data)
        
        # If 5 chunks are accumulated, process them
        if len(audio_chunks) == 5:
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
                    timeout=5,
                )
            except Exception as e:
                return f"Audio conversion error: {str(e)}", 500

            # Transcribe the WAV file
            try:
                result = model.transcribe(converted_audio, fp16=False, language="en")
                transcription_result = result['text']
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
    if transcription_result:
        return transcription_result, 200
    else:
        return "No transcription available yet.", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000 ,threaded=True, use_reloader=False)


# from flask import Flask, request, jsonify
# import subprocess
# import os
# import whisper
# import threading
# import time

# app = Flask(__name__)

# # Load the Whisper model
# model = whisper.load_model("medium")

# # Shared variables
# audio_chunks = []
# transcribe_lock = threading.Lock()
# transcription_result = None
# transcription_ready = threading.Event()

# @app.route('/audio', methods=['POST'])
# def process_audio():
#     global audio_chunks, transcription_result, transcription_ready

#     # Acquire lock to prevent concurrent processing
#     with transcribe_lock:
#         audio_chunks.append(request.data)

#         if len(audio_chunks) == 5:
#             audio_file = "audio.raw"
#             with open(audio_file, "wb") as f:
#                 for chunk in audio_chunks:
#                     f.write(chunk)

#             converted_audio = "audio.wav"
#             try:
#                 # Convert raw audio to WAV
#                 subprocess.run(
#                     ["ffmpeg", "-y", "-f", "s16le", "-ar", "16000", "-ac", "1", "-i", audio_file, converted_audio],
#                     check=True,
#                     stdout=subprocess.PIPE,
#                     stderr=subprocess.PIPE,
#                     timeout=30,
#                 )
#             except subprocess.CalledProcessError as e:
#                 transcription_result = f"Audio conversion error: {str(e)}"
#                 transcription_ready.set()  # Signal transcription failure
#                 return jsonify({"error": transcription_result}), 500

#             try:
#                 # Transcribe the WAV file
#                 result = model.transcribe(converted_audio, fp16=False, language="en")
#                 transcription_result = result["text"]
#             except Exception as e:
#                 transcription_result = f"Transcription error: {str(e)}"
#                 return jsonify({"error": transcription_result}), 500
#             finally:
#                 # Clean up files
#                 if os.path.exists(audio_file):
#                     os.remove(audio_file)
#                 if os.path.exists(converted_audio):
#                     os.remove(converted_audio)

#             audio_chunks.clear()  # Clear buffer after processing
#             transcription_ready.set()  # Signal transcription completion
#             return jsonify({"message": "Transcription completed."}), 200

#         return jsonify({"message": "Chunk received. Waiting for more chunks..."}), 200


# @app.route('/result', methods=['GET'])
# def get_transcription_result():
#     global transcription_result, transcription_ready

#     # Wait until transcription is ready
#     if transcription_ready.wait(timeout=300):  # 300 seconds max
#         response = transcription_result  # Prepare response
#         transcription_ready.clear()  # Reset the event for the next transcription
#         return jsonify({"transcription": response}), 200
#     else:
#         return jsonify({"error": "Transcription timeout or unavailable."}), 408


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

