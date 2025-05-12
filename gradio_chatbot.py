import gradio as gr
from db import get_all_diseases, save_chat
from utils import find_most_relevant_answer
import pyttsx3
import speech_recognition as sr

# Text-to-speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Chatbot logic
def chatbot_audio(question):
    diseases = get_all_diseases()
    result = find_most_relevant_answer(question, diseases)

    if result:
        answer = (
            f"Disease: {result['name']}\n"
            f"Description: {result['description']}\n"
            f"Symptoms: {result['symptoms']}\n"
            f"Treatments: {result['treatments']}"
        )
    else:
        answer = "Sorry, I couldn't find any matching information."

    save_chat(question, answer)
    speak(answer)  # Text-to-speech
    return answer

# Gradio interface with audio input
interface = gr.Interface(
    fn=chatbot_audio,
    inputs=[
        gr.Audio(source="microphone", type="text", label="Ask a medical question")
    ],
    outputs="text",
    title="Medical Chatbot with Voice"
)

interface.launch()
