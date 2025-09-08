#!/bin/bash

# SDA Backend Fix Script - Fix Import Errors and Restart Container
echo "Fixing SDA Backend import errors..."

# Go to the SDA directory
cd ~/sda

# Stop the current containers
echo "Stopping containers..."
docker-compose down

# Remove the problematic container to force rebuild
echo "Removing old container image..."
docker rmi sda_web 2>/dev/null || true

# Rebuild and start the containers
echo "Rebuilding and starting containers..."
docker-compose up -d --build

# Wait a moment for containers to start
sleep 10

# Check container status
echo "Checking container status..."
docker ps | grep sda

# Check logs for any errors
echo "Checking backend logs..."
docker logs sda_web_1 --tail 20

echo "Fix script completed!"
echo "If the backend is still not working, check the logs with: docker logs sda_web_1"
