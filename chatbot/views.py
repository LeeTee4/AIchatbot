# lee_chatbot_backend/chatbot/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import os
import logging
import time
from typing import List

logger = logging.getLogger(__name__)

# Try to import optional dependencies
try:
    import google.generativeai as genai
    import numpy as np
    GEMINI_AVAILABLE = True
    # Configure Gemini AI if available and key is set
    if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != 'your-gemini-api-key-here':
        genai.configure(api_key=settings.GEMINI_API_KEY)
        logger.info("Gemini AI configured successfully")
    else:
        logger.warning("Gemini API key not configured")
        GEMINI_AVAILABLE = False
except ImportError as e:
    logger.warning(f"Gemini AI not available: {e}")
    GEMINI_AVAILABLE = False
    import random

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    logger.warning("FAISS not available - semantic search will be disabled")
    FAISS_AVAILABLE = False

# Global variables for FAISS index (will be initialized when needed)
index = None
chunk_sources = []

# Real Gemini API function
def ask_gemini(question, context):
    if not GEMINI_AVAILABLE:
        return f"Mock response for: {question}. (Note: Gemini AI is not configured. Please set up your API key to get real AI responses.)"
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""Lee Electronics offers a wide range of electronic products and services such as TVs, smartphones, and laptops. You are a helpful assistant for Lee Electronics. Use the provided context to answer the customer's question accurately and concisely.

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
    filenames = ["internal_docs.txt", "policy_documents.txt", "product_descriptions.txt", "contact_doc.txt"]
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
    if not GEMINI_AVAILABLE:
        # Fallback to simple hash-based embedding
        import random
        random.seed(abs(hash(text)) % (10 ** 8))
        return [random.random() for _ in range(768)]
    
    try:
        # Use Gemini's embedding model for better accuracy
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        if hasattr(np, 'array'):
            return np.array(result['embedding']).astype("float32")
        else:
            return result['embedding']
    except Exception as e:
        logger.warning(f"Error generating Gemini embedding: {e}. Falling back to random embedding.")
        # Fallback to random embedding if Gemini fails
        import random
        random.seed(abs(hash(text)) % (10 ** 8))
        return [random.random() for _ in range(768)]

# Build FAISS index
def initialize_index():
    global index, chunk_sources
    if index is not None:
        return  # Already initialized
    
    if not FAISS_AVAILABLE:
        logger.warning("FAISS not available - using simple search fallback")
        # Simple fallback without FAISS
        chunk_sources = []
        all_text = load_documents()
        for doc in all_text:
            chunks = chunk_text(doc)
            chunk_sources.extend(chunks)
        return
    
    try:
        doc_chunks = []
        chunk_sources = []
        all_text = load_documents()
        for doc in all_text:
            chunks = chunk_text(doc)
            doc_chunks.extend(chunks)
            chunk_sources.extend(chunks)

        index = faiss.IndexFlatL2(768)  # Updated to match Gemini embedding dimension
        vectors = [embed_text(chunk) for chunk in doc_chunks]
        if hasattr(np, 'array'):
            index.add(np.array(vectors))
        else:
            # Convert to numpy-like array if numpy not available
            import array
            flat_vectors = []
            for vector in vectors:
                flat_vectors.extend(vector)
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
    
    if not FAISS_AVAILABLE:
        # Simple fallback search
        initialize_index()  # Make sure chunk_sources is populated
        if not chunk_sources:
            return "Default context: Lee Electronics provides quality electronic products and services."
        
        # Simple keyword matching
        question_words = question.lower().split()
        scored_chunks = []
        for chunk in chunk_sources:
            score = sum(1 for word in question_words if word in chunk.lower())
            if score > 0:
                scored_chunks.append((score, chunk))
        
        # Sort by score and take top_k
        scored_chunks.sort(reverse=True, key=lambda x: x[0])
        top_chunks = [chunk for _, chunk in scored_chunks[:top_k]]
        
        if not top_chunks:
            top_chunks = chunk_sources[:top_k]
        
        return "\n---\n".join(top_chunks)
    
    try:
        query_vector = embed_text(question)
        if hasattr(np, 'array'):
            D, I = index.search(np.array([query_vector]), top_k)
        else:
            # Fallback without numpy
            D, I = index.search([query_vector], top_k)
        return "\n---\n".join([chunk_sources[i] for i in I[0]])
    except Exception as e:
        logger.error(f"Error in retrieve_context: {e}")
        return "Default context: Lee Electronics provides quality electronic products and services."

# API Endpoint
@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(APIView):
    def post(self, request):
        try:
            question = request.data.get("question")
            if not question:
                return Response({"error": "Question is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if this is a test connection
            if question.lower().strip() == "test":
                return Response({"answer": "Connection successful! Lee Electronics AI Assistant is ready to help you."})

            context = retrieve_context(question)
            answer = ask_gemini(question, context)
            return Response({"answer": answer})
        except Exception as e:
            logger.error(f"Error in ChatbotView: {e}")
            return Response({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """Health check endpoint"""
        try:
            return Response({
                "status": "healthy",
                "message": "Lee Electronics AI Chatbot API is running",
                "endpoints": {
                    "chat": "/api/chat/ (POST)",
                    "health": "/api/chat/ (GET)"
                }
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Test endpoint for debugging
@method_decorator(csrf_exempt, name='dispatch')
class TestView(APIView):
    def get(self, request):
        return Response({
            "message": "Backend is working!",
            "timestamp": time.time(),
            "gemini_configured": bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != 'your-gemini-api-key-here')
        })
    
    def post(self, request):
        question = request.data.get("question", "No question provided")
        return Response({
            "received_question": question,
            "response": f"Echo: {question}",
            "backend_status": "working"
        })