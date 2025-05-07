import pyttsx3
import threading
import queue
import speech_recognition as sr
from flask import jsonify

speech_queue = queue.Queue()
engine = pyttsx3.init()

def speak_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

threading.Thread(target=speak_worker, daemon=True).start()

def speak(text):
    speech_queue.put(text)

def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        question = recognizer.recognize_google(audio)
        return jsonify({"question": question})
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Speech recognition error: {e}"}), 500
