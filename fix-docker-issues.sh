#!/bin/bash

# SDA Docker Fix Script - Complete Container Reset
echo "Fixing Docker container configuration issues..."

# Go to the SDA directory
cd ~/sda

echo "Step 1: Stopping all containers..."
docker-compose down --remove-orphans

echo "Step 2: Removing all SDA-related containers..."
docker ps -a | grep sda | awk '{print $1}' | xargs -r docker rm -f

echo "Step 3: Removing SDA images to force clean rebuild..."
docker images | grep sda | awk '{print $3}' | xargs -r docker rmi -f

echo "Step 4: Cleaning up Docker system..."
docker system prune -f

echo "Step 5: Removing any volume conflicts..."
docker volume ls | grep sda | awk '{print $2}' | xargs -r docker volume rm

echo "Step 6: Checking Docker Compose file..."
if [ ! -f "docker-compose.yml" ]; then
    echo "ERROR: docker-compose.yml not found!"
    echo "Available docker-compose files:"
    ls -la docker-compose*.yml
    echo "Please specify which docker-compose file to use."
    exit 1
fi

echo "Step 7: Rebuilding containers from scratch..."
docker-compose build --no-cache

echo "Step 8: Starting containers..."
docker-compose up -d

echo "Step 9: Waiting for containers to start..."
sleep 20

echo "Step 10: Checking container status..."
docker ps

echo "Step 11: Checking backend logs..."
docker logs sda_web_1 --tail 20

echo ""
echo "Docker fix completed!"
echo "If containers are running properly, test the upload endpoint:"
echo "curl http://localhost:8000/"
