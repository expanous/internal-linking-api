#!/usr/bin/env python3
"""
Railway startup script
"""

import os
import subprocess
import sys

def main():
    # Download spaCy model
    print("Downloading spaCy model...")
    try:
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
        print("spaCy model downloaded successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading spaCy model: {e}")
        # Continue anyway, the model might already be there
    
    # Get port from environment variable
    port = os.environ.get('PORT', '8000')
    print(f"PORT environment variable: {os.environ.get('PORT', 'NOT_SET')}")
    print(f"Using port: {port}")
    
    # Start uvicorn with explicit port
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "api_internal_linking:app", 
        "--host", "0.0.0.0", 
        "--port", str(port)
    ]
    print(f"Running command: {' '.join(cmd)}")
    
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main() 