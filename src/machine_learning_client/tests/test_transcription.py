# # For testing purposes, so I can get access to speech_recog testing file
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
from speech_recog import transcription

def test_transcribe_normal_hello():
    text = transcription("/Users/williamxie/Software Engineer Fall 24/4-containers-kablam/src/machine_learning_client/tests/normalAudio.wav")
    print(text);
    assert text == "hello my name is william"