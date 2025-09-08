#!/bin/bash

# Alternative Manual Fix - Step by Step
echo "Manual Docker fix for SDA container issues..."

cd ~/sda

echo "=== STEP 1: Complete cleanup ==="
echo "Stopping all containers..."
docker stop $(docker ps -aq) 2>/dev/null || true

echo "Removing all containers..."
docker rm $(docker ps -aq) 2>/dev/null || true

echo "Removing all images..."
docker rmi $(docker images -q) --force 2>/dev/null || true

echo "Cleaning Docker system..."
docker system prune -a -f --volumes

echo "=== STEP 2: Rebuild everything ==="
echo "Building without cache..."
docker-compose build --no-cache --pull

echo "=== STEP 3: Start fresh ==="
echo "Starting containers..."
docker-compose up -d

echo "=== STEP 4: Monitor startup ==="
echo "Waiting 30 seconds for startup..."
sleep 30

echo "Container status:"
docker ps

echo "Backend logs:"
docker logs sda_web_1 --tail 15 2>/dev/null || echo "Backend container not found yet"

echo ""
echo "Manual fix completed!"
