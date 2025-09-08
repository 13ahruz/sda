#!/bin/bash

# SDA Backend Complete Image Upload Fix
echo "Applying complete image upload fix..."

# Go to the SDA directory
cd ~/sda

# Set production environment variable
echo "Setting production environment..."
export ENVIRONMENT=production
export DOMAIN_URL=https://sdaconsulting.az

# Update .env file if it exists
if [ -f ".env" ]; then
    # Remove old environment variables if they exist
    sed -i '/^ENVIRONMENT=/d' .env
    sed -i '/^DOMAIN_URL=/d' .env
fi

# Add production environment variables to .env
echo "ENVIRONMENT=production" >> .env
echo "DOMAIN_URL=https://sdaconsulting.az" >> .env

echo "Environment variables set:"
cat .env | grep -E "(ENVIRONMENT|DOMAIN_URL)"

# Stop containers
echo "Stopping containers..."
docker-compose down

# Remove old container to force rebuild
echo "Removing old container image..."
docker rmi sda_web 2>/dev/null || true

# Rebuild and start containers
echo "Rebuilding and starting containers..."
docker-compose up -d --build

# Wait for containers to start
echo "Waiting for containers to start..."
sleep 15

# Check container status
echo "Checking container status..."
docker ps | grep sda

# Test the upload endpoint
echo "Testing upload endpoint..."
sleep 5
curl -s http://localhost:8000/ || echo "Backend not yet ready"

# Check logs
echo "Recent backend logs:"
docker logs sda_web_1 --tail 10

echo ""
echo "Fix applied! Please test image upload in admin panel."
echo "If still not working, check logs with: docker logs sda_web_1"
