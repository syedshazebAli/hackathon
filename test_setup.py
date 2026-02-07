import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Checking if required packages are installed...")

try:
    import qdrant_client
    print("[OK] qdrant_client imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import qdrant_client: {e}")

try:
    import groq
    print("[OK] groq imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import groq: {e}")

try:
    from sentence_transformers import SentenceTransformer
    print("[OK] sentence_transformers imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import sentence_transformers: {e}")

try:
    import fastapi
    print("[OK] fastapi imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import fastapi: {e}")

try:
    import psycopg2
    print("[OK] psycopg2 imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import psycopg2: {e}")

# Check if API keys are loaded
required_keys = ['GROQ_API_KEY', 'QDRANT_URL', 'QDRANT_API_KEY', 'NEON_DB_URL']
for key in required_keys:
    if os.getenv(key):
        print(f"[OK] {key} found in environment")
    else:
        print(f"[ERROR] {key} NOT found in environment")

print("\nPackage check complete!")