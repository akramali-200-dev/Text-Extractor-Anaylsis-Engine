# Chatbot Application

A modular AI-powered chatbot application with content analysis and text rephrasing capabilities, built with **async/await** patterns for optimal performance and **Docker** for easy deployment.

## Architecture

The application follows a clean modular architecture with full async support and Docker containerization:

```
├── config/                 # Configuration settings
│   ├── __init__.py
│   └── settings.py         # Environment variables and app settings
├── database/              # Database operations (async)
│   ├── __init__.py
│   └── db_manager.py      # Async SQLite database manager
├── services/              # External service integrations (async)
│   ├── __init__.py
│   └── ai_service.py      # Async OpenAI API service
├── models/                # Data models and schemas
│   ├── __init__.py
│   └── schemas.py         # Pydantic models
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── text_processing.py # Text processing utilities
├── api/                   # FastAPI backend (async)
│   ├── __init__.py
│   └── content_analysis_api.py # Async API endpoints
├── frontend/              # Streamlit frontend applications
│   ├── __init__.py
│   ├── components.py      # Shared UI components
│   ├── extractor_app.py   # Content analysis app (async HTTP)
│   └── rephraser_app.py   # Text rephrasing app (async AI)
├── scripts/               # Docker management scripts
│   ├── start.sh           # Service startup script
│   └── docker-manager.sh  # Docker management utility
├── main.py               # CLI entry point (async support)
├── Dockerfile            # Docker container definition
├── docker-compose.yml    # Multi-service Docker setup
├── .dockerignore         # Docker ignore patterns
├── env.example           # Environment variables template
└── requirements.txt      # Dependencies
```

## Features

### Content Analysis API (Async)
- **Analyze Text**: Extract structured metadata (title, topics, sentiment, keywords)
- **Batch Analysis**: Process multiple texts concurrently using `asyncio.gather()`
- **Search**: Query past analyses by topic or keyword
- **Database Storage**: Async SQLite database for persistence
- **High Performance**: Non-blocking I/O operations throughout

### Frontend Applications
- **Content Extractor**: Modern UI with async HTTP requests using `httpx`
- **Athena Rephraser**: Academic writing assistant with async AI calls

### Docker Deployment
- **Multi-Service Setup**: API, Extractor, and Rephraser in separate containers
- **Auto-Start**: All services start automatically with docker-compose
- **Health Checks**: Built-in health monitoring for all services
- **Volume Persistence**: Data and logs persist across container restarts
- **Easy Management**: Simple scripts for start/stop/restart operations

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key

### 1. Clone and Setup
```bash
git clone <repository-url>
cd chatbot-application
```

### 2. Configure Environment
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your OpenAI API key
nano .env
```

### 3. Start All Services
```bash
# Using the management script (recommended)
./scripts/docker-manager.sh start

# Or using docker-compose directly
docker-compose up --build -d
```

### 4. Access Applications
- **🔧 API Backend**: http://localhost:8000
- **📊 API Documentation**: http://localhost:8000/docs
- **⚡ Content Extractor**: http://localhost:8501
- **🎓 Athena Rephraser**: http://localhost:8502

## Docker Management

### Using the Management Script
```bash
# Start all services
./scripts/docker-manager.sh start

# Stop all services
./scripts/docker-manager.sh stop

# Restart all services
./scripts/docker-manager.sh restart

# View logs
./scripts/docker-manager.sh logs

# Check service status
./scripts/docker-manager.sh status

# Run tests
./scripts/docker-manager.sh test

# Clean up Docker resources
./scripts/docker-manager.sh cleanup
```

### Using Docker Compose Directly
```bash
# Start all services
docker-compose up --build -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Restart specific service
docker-compose restart api
```

## Manual Installation (Without Docker)

### Prerequisites
- Python 3.11+
- OpenAI API key

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variable
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Run Services

#### CLI Commands
```bash
# Run API server (async FastAPI)
python main.py api

# Run content extractor (async HTTP client)
python main.py extractor

# Run rephraser (async AI service)
python main.py rephraser

# Test API functionality (async test)
python main.py test
```

#### Direct Execution
```bash
# API Server (async)
uvicorn api.content_analysis_api:app --reload

# Content Extractor (async HTTP)
streamlit run frontend/extractor_app.py

# Rephraser (async AI)
streamlit run frontend/rephraser_app.py
```

## API Endpoints (All Async)

- `POST /analyze` - Analyze content (async)
- `POST /analyze_batch` - Batch analysis (concurrent processing)
- `GET /search` - Search analyses (async database queries)
- `GET /analysis/{id}` - Get specific analysis (async)
- `GET /health` - Health check (async)

## Performance Benefits

### Async Architecture Advantages:
- **Concurrent Processing**: Batch operations process multiple texts simultaneously
- **Non-blocking I/O**: Database and API calls don't block the event loop
- **Better Resource Utilization**: Handle more requests with fewer resources
- **Improved Scalability**: Better performance under high load
- **Faster Response Times**: Reduced latency for I/O-bound operations

### Docker Advantages:
- **Easy Deployment**: One command to start all services
- **Consistent Environment**: Same environment across development and production
- **Service Isolation**: Each service runs in its own container
- **Auto-Recovery**: Services restart automatically if they fail
- **Resource Management**: Better control over resource allocation

### Technical Implementation:
- **Database**: `aiosqlite` for async SQLite operations
- **HTTP Client**: `httpx` for async HTTP requests
- **AI Service**: `AsyncOpenAI` for non-blocking API calls
- **API Framework**: FastAPI with async endpoints
- **Concurrency**: `asyncio.gather()` for parallel processing
- **Containerization**: Docker with multi-service architecture

## Configuration

### Environment Variables
All settings are centralized in `config/settings.py` and can be overridden via environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `API_HOST`: API server host (default: 127.0.0.1)
- `API_PORT`: API server port (default: 8000)
- `DB_PATH`: Database file path (default: extractor.db)
- `MODEL_NAME`: OpenAI model name (default: gpt-4o-mini)

### Docker Configuration
- **Ports**: API (8000), Extractor (8501), Rephraser (8502)
- **Volumes**: Data persistence in `./data` and logs in `./logs`
- **Health Checks**: Automatic service monitoring
- **Restart Policy**: Services restart unless manually stopped

## Troubleshooting

### Common Issues

1. **OpenAI API Key Not Set**
   ```bash
   # Check if API key is set
   echo $OPENAI_API_KEY
   
   # Set API key
   export OPENAI_API_KEY="your-key-here"
   ```

2. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   
   # Stop conflicting services or change ports in docker-compose.yml
   ```

3. **Docker Services Not Starting**
   ```bash
   # Check Docker logs
   docker-compose logs
   
   # Check service status
   docker-compose ps
   
   # Restart services
   docker-compose restart
   ```

4. **Database Issues**
   ```bash
   # Check database file permissions
   ls -la data/
   
   # Remove and recreate database
   rm data/extractor.db
   docker-compose restart api
   ```

### Getting Help
- Check service logs: `./scripts/docker-manager.sh logs`
- View service status: `./scripts/docker-manager.sh status`
- Run health checks: Visit http://localhost:8000/health
- Test API functionality: `./scripts/docker-manager.sh test`
