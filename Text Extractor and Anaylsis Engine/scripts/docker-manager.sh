#!/bin/bash

# Docker management script for Chatbot Application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check if docker-compose is available
check_docker_compose() {
    if ! command -v docker-compose > /dev/null 2>&1; then
        print_error "docker-compose is not installed. Please install docker-compose and try again."
        exit 1
    fi
}

# Function to create .env file if it doesn't exist
create_env_file() {
    if [ ! -f .env ]; then
        print_status "Creating .env file..."
        cat > .env << EOF
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Application Configuration
API_HOST=0.0.0.0
API_PORT=8000
EXTRACTOR_PORT=8501
REPHRASER_PORT=8502
EOF
        print_warning "Please edit .env file and add your OpenAI API key!"
        print_warning "Run: nano .env or vim .env"
        return 1
    fi
    return 0
}

# Function to build and start all services
start_all() {
    print_status "Building and starting all services..."
    docker-compose up --build -d
    
    print_status "Waiting for services to be ready..."
    sleep 10
    
    print_success "All services started!"
    print_status "Services available at:"
    echo "  🔧 API Backend:     http://localhost:8000"
    echo "  📊 API Docs:       http://localhost:8000/docs"
    echo "  ⚡ Extractor:       http://localhost:8501"
    echo "  🎓 Rephraser:       http://localhost:8502"
}

# Function to stop all services
stop_all() {
    print_status "Stopping all services..."
    docker-compose down
    print_success "All services stopped!"
}

# Function to restart all services
restart_all() {
    print_status "Restarting all services..."
    docker-compose down
    docker-compose up --build -d
    print_success "All services restarted!"
}

# Function to show logs
show_logs() {
    local service=${1:-""}
    if [ -z "$service" ]; then
        print_status "Showing logs for all services..."
        docker-compose logs -f
    else
        print_status "Showing logs for $service..."
        docker-compose logs -f "$service"
    fi
}

# Function to show service status
show_status() {
    print_status "Service Status:"
    docker-compose ps
}

# Function to clean up
cleanup() {
    print_status "Cleaning up Docker resources..."
    docker-compose down -v --remove-orphans
    docker system prune -f
    print_success "Cleanup completed!"
}

# Function to run tests
run_tests() {
    print_status "Running API tests..."
    docker-compose exec api python main.py test
}

# Main script logic
case "$1" in
    "start")
        check_docker
        check_docker_compose
        if create_env_file; then
            start_all
        else
            print_error "Please configure .env file first!"
            exit 1
        fi
        ;;
    "stop")
        check_docker_compose
        stop_all
        ;;
    "restart")
        check_docker
        check_docker_compose
        restart_all
        ;;
    "logs")
        check_docker_compose
        show_logs "$2"
        ;;
    "status")
        check_docker_compose
        show_status
        ;;
    "test")
        check_docker_compose
        run_tests
        ;;
    "cleanup")
        check_docker_compose
        cleanup
        ;;
    "help"|"--help"|"-h"|"")
        echo "Chatbot Application Docker Management Script"
        echo ""
        echo "Usage: $0 {command}"
        echo ""
        echo "Commands:"
        echo "  start     - Build and start all services"
        echo "  stop      - Stop all services"
        echo "  restart   - Restart all services"
        echo "  logs      - Show logs (optionally for specific service)"
        echo "  status    - Show service status"
        echo "  test      - Run API tests"
        echo "  cleanup   - Clean up Docker resources"
        echo "  help      - Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 start"
        echo "  $0 logs api"
        echo "  $0 status"
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Run '$0 help' for usage information."
        exit 1
        ;;
esac
