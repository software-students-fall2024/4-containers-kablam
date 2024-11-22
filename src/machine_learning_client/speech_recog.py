import speech_recognition as sr
from flask import Flask, request, jsonify
import os
app = Flask(__name__)

def transcription(file_path):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            r.adjust_for_ambient_noise(source, duration = 0.2)
            audio = r.record(source)
            
            text = r.recognize_google(audio)
            return text.lower()

    except sr.UnknownValueError:
        raise ValueError("Audio cannot be understood")
    except sr.RequestError as e:
        raise RuntimeError(f"API error; {e}")

@app.route('/accept_file', methods=['POST'])
def accept_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['audio']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # create file path under uploads folder
    uploaded_file_path = os.path.join(os.path.dirname(__file__), 'uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    # save file at the path with name
    file.save(uploaded_file_path)

    transcription_text = transcription(uploaded_file_path)
    print("Transcription text: ", transcription_text)


    # TRANSCRIBE FILE
    

@app.route('/', methods=['GET'])
def test_server():
    return('<h1>Working</h1>')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)