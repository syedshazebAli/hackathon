#!/usr/bin/env python3
"""
Setup and startup script for the Robotics Book RAG Chatbot
"""

import os
import sys
import subprocess
import importlib.util

def check_dependency(module_name, package_name=None):
    """Check if a Python module is available"""
    if package_name is None:
        package_name = module_name
        
    spec = importlib.util.find_spec(module_name)
    return spec is not None

def main():
    print("Robotics Book RAG Chatbot - Setup and Startup")
    print("=" * 50)
    
    # Check required dependencies
    required_deps = [
        ('qdrant_client', 'qdrant-client'),
        ('groq', 'groq'),
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('psycopg2', 'psycopg2-binary'),
        ('markdown', 'markdown'),
        ('dotenv', 'python-dotenv'),
        ('sentence_transformers', 'sentence-transformers')
    ]
    
    missing_deps = []
    for module, package in required_deps:
        if not check_dependency(module):
            missing_deps.append(package)
    
    if missing_deps:
        print(f"Missing dependencies: {', '.join(missing_deps)}")
        print("\nInstall them using:")
        print(f"pip install {' '.join(missing_deps)}")
        print("\nNote: sentence-transformers may take a while to install on Windows due to PyTorch dependencies.")
        return
    
    print("All dependencies are installed!")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n.env file not found! Please create one with your API keys.")
        print("Required keys: GROQ_API_KEY, QDRANT_URL, QDRANT_API_KEY, NEON_DB_URL")
        return
    
    print("\nEnvironment file (.env) found!")
    
    # Check if docs folder exists
    if not os.path.exists('docs'):
        print("\ndocs/ folder not found. Creating an empty one...")
        os.makedirs('docs', exist_ok=True)
        print("Created docs/ folder. Please add your markdown files there.")
    
    print("\nReady to run the application!")
    print("\nTo run the full application:")
    print("1. Run: python ingest.py  # to process your documents")
    print("2. Run: uvicorn main:app --reload  # to start the server")
    print("\nThe server will be available at http://localhost:8000")
    
    # Check if the user wants to run the server now
    response = input("\nWould you like to start the server now? (y/n): ")
    if response.lower() in ['y', 'yes']:
        print("\nStarting the server...")
        subprocess.run([sys.executable, '-m', 'uvicorn', 'main:app', '--reload'])

if __name__ == '__main__':
    main()