import speech_recognition as sr

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
