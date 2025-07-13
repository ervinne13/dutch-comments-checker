#!/bin/bash
set -e

# Start Ollama in the background
ollama serve &

# Wait for Ollama to be ready
until curl -sf http://localhost:11434; do
  sleep 1
done

# Pull the llama3 model
ollama pull llama3

# Wait for background Ollama to exit (keep container running)
wait
