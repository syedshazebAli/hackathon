from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
from qdrant_client import QdrantClient
from groq import Groq
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Robotics Book RAG Chatbot", version="1.0.0")

# Initialize clients
qdrant_client = QdrantClient(
    url=os.getenv('QDRANT_URL'),
    api_key=os.getenv('QDRANT_API_KEY'),
    prefer_grpc=True
)

groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# For now, we'll use a mock embedding function until sentence-transformers is installed
def get_embeddings(text):
    """
    Mock embedding function - replace with actual sentence transformer when available
    This is just a placeholder to allow the server to start
    """
    # Return a simple mock embedding (in real implementation, use sentence-transformers)
    return [0.0] * 384  # Assuming 384-dim embeddings like MiniLM

# Connect to Neon Postgres database
def get_db_connection():
    conn = psycopg2.connect(
        os.getenv('NEON_DB_URL'),
        cursor_factory=RealDictCursor
    )
    return conn

# Create chat history table if it doesn't exist
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            session_id VARCHAR(255) NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

# Initialize database
init_db()

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        user_message = request.message
        
        # Generate mock embedding for the user query (will be replaced with real embeddings)
        query_embedding = get_embeddings(user_message)
        
        # Search in Qdrant for relevant documents
        # Note: This will only work properly once documents are ingested with real embeddings
        try:
            search_results = qdrant_client.search(
                collection_name='robotics_book',
                query_vector=query_embedding,
                limit=5  # Retrieve top 5 most relevant chunks
            )
            
            # Format context from search results
            context_parts = []
            sources = []
            
            for result in search_results:
                content = result.payload.get('content', '')
                source = result.payload.get('source', 'Unknown')
                title = result.payload.get('title', 'Untitled')
                
                context_parts.append(content)
                sources.append({
                    'title': title,
                    'source': source,
                    'relevance_score': result.score
                })
            
            context = "\n\n".join(context_parts)
        except Exception as e:
            # If collection doesn't exist yet, use empty context
            context = ""
            sources = []
            print(f"Warning: Could not search Qdrant collection: {e}")
        
        # Prepare the prompt for Groq
        system_prompt = """You are a helpful assistant for a robotics book. Use the provided context to answer questions accurately. 
        If the context doesn't contain enough information to answer the question, say so. 
        Be concise but informative in your responses."""
        
        prompt = f"""Context: {context}\n\nQuestion: {user_message}\n\nAnswer:"""
        
        # Call Groq API to generate response
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",  # Using Llama 3 8B model as requested
            temperature=0.7,
            max_tokens=1024
        )
        
        bot_response = chat_completion.choices[0].message.content
        
        # Save chat history to database
        session_id = request.session_id or str(uuid.uuid4())
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO chat_history (session_id, user_message, bot_response)
            VALUES (%s, %s, %s)
        """, (session_id, user_message, bot_response))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return ChatResponse(response=bot_response, sources=sources)
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Robotics Book RAG Chatbot API - Ready to install sentence-transformers"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)