import speech_recognition as sr
from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["swearDB"] 
swears_collection = db["swears"]

def transcription(file_path):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            r.adjust_for_ambient_noise(source, duration = 0.2)
            audio = r.record(source)
            
            try:
               text = r.recognize_google(audio)
               return text.lower()
            except sr.UnknownValueError:
               # Log the error and return an empty string or None
               print(f"Warning: Could not understand audio in {file_path}")
               return None


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

    # SWEAR WORDS TO DETECT
    detectWords = ["hello","apple", "orange","goodbye","test"];

    transcription_split = transcription_text.split();

    for detectWord in detectWords:
        count = transcription_split.count(detectWord);
        if count > 0:
            if swears_collection.find_one({"word":detectWord}):
                swears_collection.update_one({"word":detectWord},{"$inc":{"count":count}})
            else:
                swears_collection.insert_one({"word":detectWord,"count":1})

    return jsonify({"transcription": transcription_text}), 200


@app.route('/', methods=['GET'])
def test_server():
    return('<h1>Working</h1>')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)