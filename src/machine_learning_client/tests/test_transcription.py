import os
import pytest
from speech_recog import transcription
# Get the directory where the current script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the audio file
audio_file_path = os.path.join(current_dir, "normalAudio.wav")

def test_transcribe_normal_hello():
    text = transcription(audio_file_path)
    print(audio_file_path)
    print(text);
    assert text == "hello my name is william"