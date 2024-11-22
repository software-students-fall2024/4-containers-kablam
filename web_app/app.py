# for test only (in order to enable app.py to find the src folder without build the image)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# for project use
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
# from speech_recog import transcription
import requests
#import os
import subprocess
#import speech_recognition as sr

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017/")
db = client["swearDB"] 
swears_collection = db["swears"]

@app.route("/")
def index():
    print(os.path.join(os.path.dirname(__file__), 'uploads'))
    total_swears = sum(doc["count"] for doc in swears_collection.find())
    return render_template("index.html", swears=total_swears)

@app.route("/api/swears", methods=["GET"])
def get_swear_counts():
    # docs = swears_collection.find()
    # for doc in docs:
    #     print(doc)
    swear_counts = {doc["word"]: doc["count"] for doc in swears_collection.find()}
    return jsonify(swear_counts)

@app.route('/upload', methods=['POST'])
def upload_audio():
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

    try:        
        # Create file path for converted file by replacing file extensions
        converted_file_path = uploaded_file_path.replace('.webm', '.wav')
        try:
            # Convert webm to wav with ffmpeg
            # Taken from StackOverflow
            ffmpeg_command = [
                "ffmpeg", "-y", "-i", uploaded_file_path, "-vn", "-ar", "48000", 
                "-ac", "2", "-b:a", "128k", converted_file_path
            ]
            # Run ffmpeg command
            subprocess.run(ffmpeg_command, check=True)
            print(f"Converted file: {converted_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg conversion failed: {e}")

        # Remove the original uploaded file after conversion
        os.remove(uploaded_file_path)

        # Open file to be sent to ML server
        with open(converted_file_path, 'rb') as audio_file:
            files = {'audio': (os.path.basename(converted_file_path), audio_file, 'audio/wav')}
            url = "http://speech:8080/accept_file"
            response = requests.post(url, files=files)
            if response.status_code == 200:
               transcription = response.json()['transcription']
               print(transcription)
               if(transcription is not None):
                   pass # Upload to db here?
               return jsonify("Uploaded successfully"), 200
            else:
                return jsonify("Failed to transcribe"), 400

   
    except Exception as e:
        print(f"Error during processing: {e}")
        return jsonify({"error": f"Error processing the audio file: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
