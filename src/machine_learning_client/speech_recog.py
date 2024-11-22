import speech_recognition as sr
from flask import Flask, request, jsonify

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
    # TRANSCRIBE FILE

@app.route('/', methods=['GET'])
def test_server():
    return('<h1>Working</h1>')    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)