# for test only (in order to enable app.py to find the src folder without build the image)
import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# for project use
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from src.machine_learning_client.speech_recog import transcription
#import os
import subprocess

app = Flask(__name__)
#client = MongoClient("mongodb://localhost:27017/")
client = MongoClient("mongodb://mongo:27017/")

db = client["swearDB"] 
swears_collection = db["swears"]
#user_input = db["audio and transcription"]

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
        return jsonify({"message": "File successfully converted!", "file_path": converted_file_path}), 200
    except Exception as e:
        print(f"Error during processing: {e}")
        return jsonify({"error": f"Error processing the audio file: {str(e)}"}), 500

@app.route('/transcription', methods = ['GET'])
def transcription():
    try:
        transcription_data = db["audio and transcription"].find_one({},{"transcription":1})
        return jsonify({"transcription": transcription_data["transcription"]}), 200
    except Exception as e:
        return jsonify({"error": f"Error retrieving transcriptions: {str(e)}"}), 500
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)