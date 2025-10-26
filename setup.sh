#!/bin/bash

echo "========================================="
echo "QuantEdge Trading Simulator Setup"
echo "========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker and Docker Compose found"

# Create necessary directories
echo "Creating directory structure..."
mkdir -p backend/data/raw
mkdir -p backend/data/processed
mkdir -p backend/data/models
mkdir -p backend/logs

echo "✓ Directories created"

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# QuantEdge Configuration
DATABASE_URL=sqlite+aiosqlite:///./data/quantedge.db
VITE_API_URL=http://localhost:8000
INITIAL_CAPITAL=100000
EOF
    echo "✓ .env file created"
fi

# Build and start containers
echo "Building Docker containers..."
docker-compose build

echo "Starting QuantEdge services..."
docker-compose up -d

echo ""
echo "========================================="
echo "✓ QuantEdge Setup Complete!"
echo "========================================="
echo ""
echo "Services are starting up..."
echo "  - Backend API: http://localhost:8000"
echo "  - Frontend Dashboard: http://localhost:3000"
echo "  - API Documentation: http://localhost:8000/docs"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop services:"
echo "  docker-compose down"
echo ""
echo "Happy trading! 📈"
