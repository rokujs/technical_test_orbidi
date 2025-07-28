#!/bin/sh

alias uv="/root/.local/bin/uv"

# Install dependencies
echo "Installing dependencies..."
uv sync

# run server
echo "Starting FastAPI server..."
uv run fastapi dev main.py --port 8000 --host 0.0.0.0