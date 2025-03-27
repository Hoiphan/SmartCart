import speech_recognition as sr
import pyaudio



def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("noi: ")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio,language="vi-VI")
        return text
    except:
        return None

