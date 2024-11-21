import requests
from pymongo import MongoClient
import speech_recognition as sr

#client = MongoClient("mongodb://localhost:27017/")
client = MongoClient("mongodb://mongo:27017/")

db = client["swearDB"]
user_input = db["audio and transcription"]

url = "http://web_app:3000/upload"

#data = request.get(url).json()
response = requests.get(url)
if response.status_code != 200:
    raise RuntimeError(f"Failed to fetch file path: {response.text}")
data = response.json()

if "file_path" in data:
    file_path = data["file_path"]
else:
    raise ValueError("No audio file found")

r = sr.Recognizer()
try:
    with sr.AudioFile(file_path) as source:
        r.adjust_for_ambient_noise(source, duration = 0.2)
        audio = r.record(source)
        
        text = r.recognize_google(audio)
        transciption_text = text.lower()

        input_data={
            'audio': file_path,
            'transcription': transcription_text,
        }
        db["audio and transcription"].insert_one(input_data)

except sr.UnknownValueError:
    raise ValueError("Audio cannot be understood")
except sr.RequestError as e:
    raise RuntimeError(f"API error; {e}")
