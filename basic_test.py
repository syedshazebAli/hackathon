import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Testing basic imports...")

try:
    import qdrant_client
    print("[OK] qdrant_client imported successfully")
    
    # Test connecting to Qdrant
    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_api_key = os.getenv('QDRANT_API_KEY')
    
    if qdrant_url and qdrant_api_key:
        print("[OK] Qdrant credentials found in environment")
    else:
        print("[ERROR] Qdrant credentials NOT found in environment")
        
except ImportError as e:
    print(f"[ERROR] Failed to import qdrant_client: {e}")

try:
    import groq
    print("[OK] groq imported successfully")
    
    # Test if Groq API key is available
    groq_api_key = os.getenv('GROQ_API_KEY')
    if groq_api_key:
        print("[OK] Groq API key found in environment")
    else:
        print("[ERROR] Groq API key NOT found in environment")
        
except ImportError as e:
    print(f"[ERROR] Failed to import groq: {e}")

try:
    import fastapi
    print("[OK] fastapi imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import fastapi: {e}")

try:
    import psycopg2
    print("[OK] psycopg2 imported successfully")
    
    # Test if DB URL is available
    db_url = os.getenv('NEON_DB_URL')
    if db_url:
        print("[OK] Neon DB URL found in environment")
    else:
        print("[ERROR] Neon DB URL NOT found in environment")
        
except ImportError as e:
    print(f"[ERROR] Failed to import psycopg2: {e}")

print("\nBasic functionality test complete!")