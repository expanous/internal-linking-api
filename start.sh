#!/bin/bash

# Download spaCy model if not present
python -m spacy download en_core_web_sm

# Start the API server
uvicorn api_internal_linking:app --host 0.0.0.0 --port ${PORT:-8000} 