# utils.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load BERT model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Embed disease info only once and cache it
def embed_diseases(diseases):
    disease_texts = [
        f"{d['name']} {d['description']} {d['symptoms']} {d['treatments']}"
        for d in diseases
    ]
    embeddings = model.encode(disease_texts)
    return embeddings

def find_most_relevant_answer(question, diseases):
    if not diseases:
        return None

    # Embed the diseases
    disease_embeddings = embed_diseases(diseases)

    # Embed the question
    question_embedding = model.encode([question])

    # Compute cosine similarity
    similarities = cosine_similarity(question_embedding, disease_embeddings)[0]

    # Get the most similar index
    best_idx = np.argmax(similarities)

    # Return the best matching disease
    return diseases[best_idx]
