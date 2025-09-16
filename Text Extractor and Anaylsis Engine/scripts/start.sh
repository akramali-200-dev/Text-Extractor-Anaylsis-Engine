#!/bin/bash

# Docker startup script for Chatbot Application
# This script handles environment setup and service startup

set -e

echo "🚀 Starting Chatbot Application..."

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY environment variable is not set!"
    echo "Please set your OpenAI API key:"
    echo "export OPENAI_API_KEY='your-api-key-here'"
    exit 1
fi

echo "✅ OpenAI API key is configured"

# Create necessary directories
mkdir -p data logs

# Set proper permissions
chmod 755 data logs

echo "📁 Created data and logs directories"

# Function to wait for service to be ready
wait_for_service() {
    local service_name=$1
    local port=$2
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "http://localhost:$port" > /dev/null 2>&1; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        
        echo "Attempt $attempt/$max_attempts - $service_name not ready yet..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ $service_name failed to start within expected time"
    return 1
}

# Start services based on command
case "$1" in
    "api")
        echo "🔧 Starting FastAPI Backend..."
        python main.py api
        ;;
    "extractor")
        echo "🔧 Starting Content Extractor..."
        python main.py extractor
        ;;
    "rephraser")
        echo "🔧 Starting Athena Rephraser..."
        python main.py rephraser
        ;;
    "all")
        echo "🔧 Starting all services..."
        echo "This should be run with docker-compose"
        ;;
    *)
        echo "Usage: $0 {api|extractor|rephraser|all}"
        echo "Available commands:"
        echo "  api       - Start FastAPI backend"
        echo "  extractor - Start content extractor frontend"
        echo "  rephraser - Start Athena rephraser frontend"
        echo "  all       - Start all services (use docker-compose)"
        exit 1
        ;;
esac
