# backend/app.py

import json
import sys
from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import ollama # Import the new ollama library

# --- CONFIGURATION ---
# The model you are running in Ollama
OLLAMA_MODEL = 'gemma3:4b' # Change this to your desired Ollama model

FAQ_FILE = 'faqs.json'
MODEL_NAME = 'all-MiniLM-L6-v2' # For embeddings

# --- INITIALIZATION ---
app = Flask(__name__)

# Load FAQs from the JSON file
try:
    with open(FAQ_FILE, 'r', encoding='utf-8') as f:
        faqs = json.load(f)
    print(f"Loaded {len(faqs)} FAQs from {FAQ_FILE}")
except FileNotFoundError:
    print(f"Error: The file '{FAQ_FILE}' was not found in the backend directory.")
    faqs = []
except json.JSONDecodeError:
    print(f"Error: The file '{FAQ_FILE}' is not a valid JSON file.")
    faqs = []

# Gracefully exit if no data is loaded
if not faqs:
    print("\nNo FAQs were loaded. The application cannot start without data.")
    print(f"Please make sure '{FAQ_FILE}' exists and contains valid JSON.")
    sys.exit(1)

# Prepare data for embedding
faq_questions = [item['question'] for item in faqs]

# Load the sentence transformer model
print(f"Loading sentence transformer model: {MODEL_NAME}...")
model = SentenceTransformer(MODEL_NAME)
print("Model loaded.")

# Generate embeddings for all FAQ questions
print("Generating embeddings for all FAQs...")
faq_embeddings = model.encode(faq_questions, convert_to_tensor=False)
print(f"Embeddings generated with shape: {faq_embeddings.shape}")

# Create a FAISS index for efficient similarity search
index = faiss.IndexFlatL2(faq_embeddings.shape[1])
index.add(np.array(faq_embeddings))
print("FAISS index created and populated.")


# --- RAG CORE FUNCTIONS ---

def retrieve_most_relevant_faq(user_query, k=1):
    """
    Retrieves the most relevant FAQ(s) from the FAISS index.
    """
    query_embedding = model.encode([user_query])
    D, I = index.search(query_embedding, k)
    retrieved_faq_index = I[0][0]
    return faqs[retrieved_faq_index]

def generate_response(user_query, retrieved_faq):
    """
    Generates a response using the Ollama LLM with the retrieved context.
    """
    system_prompt = "You are a helpful FAQ assistant. A user has a question, and you have found the most relevant information from a knowledge base. Answer the user's question naturally, using only the provided information. Do not mention that you are using a knowledge base."
    
    # This prompt structure is clear and effective for RAG
    prompt = f"""
    Using the following context, answer the user's question.
    
    Context:
    - Question: "{retrieved_faq['question']}"
    - Answer: "{retrieved_faq['answer']}"

    User Question: "{user_query}"
    """
    
    try:
        # Use the ollama library to stream the response
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt},
            ]
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        return "Sorry, I'm having trouble connecting to my brain right now. Please make sure the Ollama server is running."

# --- API ENDPOINT ---

@app.route('/chat', methods=['POST'])
def chat():
    """
    The main chat endpoint for the frontend to call.
    """
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    print(f"\n[USER]: {user_message}")

    # 1. Retrieve
    retrieved_faq = retrieve_most_relevant_faq(user_message)
    print(f"[RETRIEVED]: {retrieved_faq['question']}")

    # 2. Generate
    bot_response = generate_response(user_message, retrieved_faq)
    print(f"[GENERATED]: {bot_response}")

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    # Using port 5001 to avoid conflicts
    app.run(host='0.0.0.0', port=5001, debug=True)
