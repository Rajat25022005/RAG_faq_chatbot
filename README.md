RAG FAQ Chatbot (with Ollama)
This project uses a Retrieval-Augmented Generation (RAG) approach to create a chatbot that answers questions based on a provided list of FAQs. This version is configured to use Ollama to run the local Large Language Model.

How It Works
Backend (Python/Flask):

Loads your FAQs from faqs.json.

Uses sentence-transformers to create vector embeddings from the FAQs.

Builds a faiss-cpu index for fast similarity searching (the Retrieval step).

When you ask a question, it finds the most relevant FAQ.

It then sends your question and the retrieved FAQ to your local Ollama model (e.g., gemma:2b).

The Ollama model generates a natural, conversational answer (the Generation step).

Frontend (HTML/JS/CSS):

Provides a simple chat UI in your browser.

Communicates with the backend to get chatbot responses.

Setup Instructions
Step 1: Set Up Ollama
Install Ollama: If you haven't already, download and install Ollama from ollama.com.

Pull a Model: Open your terminal and pull the model you want to use. For gemma:2b, run:

ollama pull gemma:2b

Ollama will automatically start a server in the background. You can check that it's running by visiting http://localhost:11434 in your browser.

Step 2: Set Up the Backend
Create and Activate Virtual Environment:
Make sure you are inside your backend directory and your Python virtual environment is active.

macOS/Linux: source venv/bin/activate

Windows: venv\Scripts\activate

Install/Update Dependencies:
This version uses a new library for Ollama. Run the following command to install it:

pip install -r requirements.txt

Add Your FAQs:
Make sure your backend/faqs.json file is populated with your own questions and answers.

Run the Backend Server:
In the same terminal, run the Flask app:

python app.py

The server will start on http://127.0.0.1:5001.

Step 3: Launch the Frontend
Navigate to the frontend directory.

Open index.html in your web browser.

You can now chat with your FAQ bot, powered by Ollama and Gemma!