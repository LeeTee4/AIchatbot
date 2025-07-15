# 🤖 Lee Electronics AI Chatbot

A sophisticated AI-powered customer support chatbot built with Django REST Framework and Google's Gemini AI. This intelligent chatbot provides contextual responses by leveraging semantic search through a knowledge base of company documents.

## 🌟 Features

- **🧠 AI-Powered Responses**: Utilizes Google Gemini 1.5 Flash for natural, contextual conversations
- **🔍 Semantic Search**: FAISS-powered vector search with Gemini embeddings for accurate context retrieval
- **📚 Knowledge Base Integration**: Automatically processes internal documents, policies, and product descriptions
- **🛡️ Error Handling**: Robust error handling with graceful fallbacks
- **🌐 RESTful API**: Clean Django REST Framework implementation
- **🔧 Production Ready**: Environment variable configuration and proper logging

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django API     │    │   Gemini AI     │
│   (Any Client)  │◄──►│   ChatbotView    │◄──►│   GPT Model     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                          │
                              ▼                          │
                       ┌──────────────────┐              │
                       │   FAISS Index    │              │
                       │   Vector Search  │              │
                       └──────────────────┘              │
                              │                          │
                              ▼                          │
                       ┌──────────────────┐              │
                       │  Knowledge Base  │              │
                       │   - Internal     │◄─────────────┘
                       │   - Policies     │   Embeddings
                       │   - Products     │
                       └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))


## 📁 Project Structure

```
Lee_Chat/
│
├── chatbot/                    # Main chatbot application
│   ├── knowledgeBase/         # Document storage
│   │   ├── internal_docs.txt  # Internal procedures
│   │   ├── policy_documents.txt # Company policies
│   │   └── product_descriptions.txt # Product catalog
│   ├── views.py               # API endpoints & AI logic
│   ├── urls.py                # URL routing
│   └── ...
│
├── Lee_Chat/                  # Django project settings
│   ├── settings.py           # Configuration
│   ├── urls.py               # Main URL routing
│   └── ...
│
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
└── README.md               # This file
```


## 🎯 Use Cases

- **Customer Support**: Automated responses to common inquiries
- **Product Information**: Detailed product specifications and comparisons
- **Policy Clarification**: Company policies and procedures
- **Troubleshooting**: Technical support and problem resolution
- **Internal Knowledge**: Employee self-service for company informatio
