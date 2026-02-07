import os
import glob
from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import markdown

# Load environment variables
load_dotenv()

def read_markdown_files(docs_folder):
    """Read all markdown files in the docs folder"""
    md_files = glob.glob(os.path.join(docs_folder, "**/*.md"), recursive=True)
    documents = []
    
    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract title from first heading or filename
            title = Path(file_path).stem
            # Try to extract first heading as title
            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    title = line[2:].strip()
                    break
            
            documents.append({
                'id': str(hash(content) % 1000000),  # Simple hash-based ID
                'title': title,
                'content': content,
                'source': file_path
            })
    
    return documents

def chunk_text(text, max_length=500):
    """Split text into chunks of max_length characters"""
    chunks = []
    paragraphs = text.split('\n\n')
    
    current_chunk = ""
    for paragraph in paragraphs:
        if len(current_chunk + paragraph) < max_length:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def main():
    # Initialize the embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Initialize Qdrant client
    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_api_key = os.getenv('QDRANT_API_KEY')
    
    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=True
    )
    
    # Define collection name
    collection_name = 'robotics_book'
    
    # Check if collection exists, create if not
    try:
        client.get_collection(collection_name)
        print(f"Collection '{collection_name}' exists. Clearing existing vectors.")
        client.delete_collection(collection_name)
    except:
        print(f"Collection '{collection_name}' does not exist. Creating new collection.")
    
    # Create collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=model.get_sentence_embedding_dimension(), distance=models.Distance.COSINE),
    )
    
    # Read markdown files from docs folder
    docs_folder = './docs'  # Adjust this path as needed
    if not os.path.exists(docs_folder):
        print(f"Docs folder '{docs_folder}' not found. Creating empty folder.")
        os.makedirs(docs_folder, exist_ok=True)
        return
    
    documents = read_markdown_files(docs_folder)
    points = []
    
    for doc in documents:
        # Chunk the document content
        chunks = chunk_text(doc['content'])
        
        for i, chunk in enumerate(chunks):
            # Generate embedding for the chunk
            embedding = model.encode(chunk).tolist()
            
            # Create a point for Qdrant
            point = models.PointStruct(
                id=int(f"{doc['id']}{i:03d}"),  # Combine doc id and chunk index
                vector=embedding,
                payload={
                    'title': doc['title'],
                    'content': chunk,
                    'source': doc['source'],
                    'chunk_index': i
                }
            )
            points.append(point)
    
    # Upload points to Qdrant
    print(f"Uploading {len(points)} vectors to Qdrant...")
    client.upload_points(
        collection_name=collection_name,
        points=points,
        batch_size=10
    )
    
    print(f"Successfully uploaded {len(points)} vectors to collection '{collection_name}'")

if __name__ == "__main__":
    main()