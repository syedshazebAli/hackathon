# Robotics Book RAG Chatbot

This is a Retrieval-Augmented Generation (RAG) chatbot for your robotics book. It uses FastAPI, Qdrant for vector storage, Groq for inference, and Neon Postgres for chat history.

## Features

- Scans `/docs` folder for markdown files
- Creates embeddings using sentence-transformers
- Stores embeddings in Qdrant vector database
- Retrieves relevant context for user queries
- Generates responses using Groq's Llama 3 model
- Saves chat history to Neon Postgres database
- Includes a React chat widget for Docusaurus sites

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have a `/docs` folder with your robotics book markdown files

3. Run the ingestion script to process your documents:
```bash
python ingest.py
```

4. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

5. The API will be available at `http://localhost:8000`

## Usage

### API Endpoint
- POST `/chat` - Send a message and receive a response
- Request body: `{"message": "your question", "session_id": "optional session id"}`
- Response: `{"response": "answer", "sources": [{"title": "...", "source": "...", "relevance_score": ...}]}`

### Frontend Integration
The `ChatWidget.js` component can be integrated into your Docusaurus site. It connects to `http://localhost:8000/chat`.

## Quick Start

Run the following command to check your setup and start the application:

```bash
python start_app.py
```

## Components

- `.env` - Contains API keys and configuration
- `ingest.py` - Script to process documents and store embeddings
- `main.py` - FastAPI server with chat endpoint
- `ChatWidget.js` - React component for the chat interface
- `ChatWidget.css` - Styles for the chat widget
- `start_app.py` - Helper script to check dependencies and start the app
- `requirements.txt` - Python dependencies