from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def find_most_relevant_answer(question, diseases):
    docs = [f"{d['name']} {d['description']} {d['symptoms']} {d['treatments']}" for d in diseases]
    if not docs:
        return None

    embeddings = model.encode(docs, convert_to_tensor=True)
    question_embedding = model.encode(question, convert_to_tensor=True)
    similarities = np.dot(embeddings, question_embedding.reshape(-1, 1))

    most_similar_idx = np.argmax(similarities)

    return diseases[most_similar_idx]
