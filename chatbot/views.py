# lee_chatbot_backend/chatbot/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import numpy as np
from django.conf import settings
import os
import logging
import google.generativeai as genai
import time
from typing import List

logger = logging.getLogger(__name__)

# Configure Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)

# Global variables for FAISS index (will be initialized when needed)
index = None
chunk_sources = []

# Real Gemini API function
def ask_gemini(question, context):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""You are a helpful assistant for Lee Electronics. Use the provided context to answer the customer's question accurately and concisely.

Context:
{context}

Customer Question: {question}

Please provide a helpful and accurate response based on the context above. If the context doesn't contain enough information to answer the question, say so politely and suggest contacting customer support."""

        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return f"I apologize, but I'm having trouble processing your request right now. Please try again later or contact our customer support team."

# Load documents and chunk them
def load_documents():
    docs_path = os.path.join(settings.BASE_DIR, "chatbot", "knowledgeBase")
    filenames = ["internal_docs.txt", "policy_documents.txt", "product_descriptions.txt"]
    content = []
    
    for file in filenames:
        file_path = os.path.join(docs_path, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content.append(f.read())
        except FileNotFoundError:
            logger.warning(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
    
    if not content:
        logger.warning("No knowledge base documents found")
        return ["Default knowledge: Lee Electronics is a technology company."]
    
    return content

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Generate embeddings using Gemini
def embed_text(text):
    try:
        # Use Gemini's embedding model for better accuracy
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return np.array(result['embedding']).astype("float32")
    except Exception as e:
        logger.warning(f"Error generating Gemini embedding: {e}. Falling back to random embedding.")
        # Fallback to random embedding if Gemini fails
        np.random.seed(abs(hash(text)) % (10 ** 8))
        return np.random.rand(768).astype("float32")  # Gemini embeddings are 768-dimensional

# Build FAISS index
def initialize_index():
    global index, chunk_sources
    if index is not None:
        return  # Already initialized
    
    try:
        import faiss
        
        doc_chunks = []
        chunk_sources = []
        all_text = load_documents()
        for doc in all_text:
            chunks = chunk_text(doc)
            doc_chunks.extend(chunks)
            chunk_sources.extend(chunks)

        index = faiss.IndexFlatL2(768)  # Updated to match Gemini embedding dimension
        vectors = [embed_text(chunk) for chunk in doc_chunks]
        index.add(np.array(vectors))
        logger.info("FAISS index initialized successfully")
    except ImportError:
        logger.error("FAISS not installed. Please install with: pip install faiss-cpu")
        raise
    except Exception as e:
        logger.error(f"Error initializing index: {e}")
        raise

# Retrieve relevant chunks
def retrieve_context(question, top_k=3):
    initialize_index()  # Ensure index is initialized
    query_vector = embed_text(question)
    D, I = index.search(np.array([query_vector]), top_k)
    return "\n---\n".join([chunk_sources[i] for i in I[0]])

# API Endpoint
class ChatbotView(APIView):
    def post(self, request):
        try:
            question = request.data.get("question")
            if not question:
                return Response({"error": "Question is required."}, status=status.HTTP_400_BAD_REQUEST)

            context = retrieve_context(question)
            answer = ask_gemini(question, context)
            return Response({"answer": answer})
        except Exception as e:
            logger.error(f"Error in ChatbotView: {e}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

