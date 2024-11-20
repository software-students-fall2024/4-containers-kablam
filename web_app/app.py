# for test only (in order to enable app.py to find the src folder without build the image)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# for project use
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from src.machine_learning_client.speech_recog import transcription
#import os
import subprocess
#import speech_recognition as sr

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["swearDB"] 
swears_collection = db["swears"]
user_input = db["audio and transcription"]

@app.route("/")
def index():
    total_swears = sum(doc["count"] for doc in swears_collection.find())
    #return render_template("index.html", swears=total_swears)
    return render_template("index.html", swears=0)

@app.route("/api/swears", methods=["GET"])
def get_swear_counts():
    docs = swears_collection.find()
    for doc in docs:
        print(doc)
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
    uploaded_file_path = os.path.join('uploads', file.filename)
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
   
        #immediately transcribe the audio file without saving it to the database
        transcription_text = transcription(converted_file_path)
        #save both .wav audio file and transcription to db
        input_data={
            'audio': converted_file_path,
            'transcription': transcription_text,
        }
        db["audio and transcription"].insert_one(input_data)
        print(transcription_text)
        return jsonify({"transcription": transcription_text}), 200

        #return jsonify({"message": "File successfully converted!", "file_path": converted_file_path}), 200
    excep