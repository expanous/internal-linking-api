#!/usr/bin/env python3
"""
Startup script for Railway deployment
"""

import os
import subprocess
import sys

def main():
    # Download spaCy model
    print("Downloading spaCy model...")
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
    
    # Get port from environment variable
    port = os.environ.get('PORT', '8000')
    print(f"Starting server on port {port}")
    
    # Start uvicorn
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "api_internal_linking:app", 
        "--host", "0.0.0.0", 
        "--port", port
    ], check=True)

if __name__ == "__main__":
    main() 