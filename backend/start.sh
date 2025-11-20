#!/bin/bash

# Script to initialize and start the backend server
# This ensures data is downloaded before starting the server

echo "Starting IMDB AI Backend..."

# Download data files if needed
python download_data.py

# Start the FastAPI server
uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
