import speech_recognition as sr
import pyttsx3

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to listen to the user's voice and convert it to text
def listen():
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I could not understand that.")
            return None

# Function to speak the bot's response
def speak(text):
    engine.say(text)
    engine.runAndWait()


import requests
from bs4 import BeautifulSoup

# Function to scrape articles from Healthline (or another medical site)
def fetch_articles():
    url = 'https://www.healthline.com/something'  # Change this URL to a medical article listing
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for article_tag in soup.find_all('article'):  # Adjust based on the site structure
        title = article_tag.find('h2').get_text()
        content = article_tag.find('div', {'class': 'article-content'}).get_text()
        articles.append({'title': title, 'content': content})
    
    print(f"Found {len(articles)} articles.")
    return articles


import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Initialize models
embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
gpt_model = GPT2LMHeadModel.from_pretrained('gpt2')
gpt_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Function to create FAISS index from articles
def create_faiss_index(articles):
    # Generate embeddings for articles
    embeddings = embedding_model.encode([article['content'] for article in articles])
    faiss_index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 distance
    faiss_index.add(np.array(embeddings))
    return faiss_index

# Function to generate a response from the LLM using the retrieved article
def generate_response(query, faiss_index, articles):
    # Convert query to embedding
    query_embedding = embedding_model.encode([query])
    _, indices = faiss_index.search(np.array(query_embedding), k=1)  # Search for the closest article
    relevant_article = articles[indices[0][0]]  # Fetch the relevant article
    
    # Use GPT-2 to generate a response based on the relevant article
    inputs = gpt_tokenizer.encode(relevant_article['content'], return_tensors='pt')
    outputs = gpt_model.generate(inputs, max_length=150, num_return_sequences=1)
    return gpt_tokenizer.decode(outputs[0], skip_special_tokens=True)


# Example patient data
patient_data = {
    'patient_id': '12345',
    'name': 'John Doe',
    'health_data': {
        'diagnoses': ['Hypertension'],
        'medications': ['Amlodipine'],
        'allergies': ['Penicillin']
    }
}

# Function to fetch patient data (simulate interaction with digital twin)
def get_patient_data(patient_id):
    if patient_data['patient_id'] == patient_id:
        return patient_data
    else:
        return None


from flask import Flask, request, jsonify

app = Flask(__name__)

# Route to handle user queries
@app.route('/query', methods=['POST'])
def handle_query():
    user_query = request.json.get('query', '')  # Get user query from JSON body
    if not user_query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Fetch the articles from the medical site
    articles = fetch_articles()
    faiss_index = create_faiss_index(articles)
    
    # Get the response from the LLM using RAG
    response = generate_response(user_query, faiss_index, articles)
    
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
