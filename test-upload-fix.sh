#!/bin/bash

# Test Upload Fix Script
echo "Testing upload URL generation fix..."

cd ~/sda

echo "=== Current uploads structure ==="
echo "Files in uploads directory:"
find uploads -type f -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" | head -10

echo ""
echo "=== Deploying fix ==="
echo "Restarting backend container with fixes..."
docker-compose restart web

echo "Waiting for container to start..."
sleep 10

echo ""
echo "=== Testing upload endpoint ==="
echo "Testing basic API:"
curl -s http://localhost:8000/ || echo "API not responding"

echo ""
echo "=== Check container logs ==="
echo "Recent backend logs:"
docker logs sda_web_1 --tail 15 2>/dev/null || echo "Container logs not available"

echo ""
echo "=== Check file accessibility ==="
echo "Checking if existing files are accessible via nginx:"

# Test one of the existing files
EXISTING_FILE=$(find uploads -name "*.png" | head -1 | sed 's|uploads/||')
if [ ! -z "$EXISTING_FILE" ]; then
    echo "Testing file access: https://sdaconsulting.az/uploads/$EXISTING_FILE"
    curl -I -s https://sdaconsulting.az/uploads/$EXISTING_FILE | head -3
else
    echo "No test files found"
fi

echo ""
echo "=== Instructions ==="
echo "1. Try uploading a new image in admin panel"
echo "2. Check the generated URL format"
echo "3. Verify the image is accessible at the URL"
echo ""
echo "Expected URL format: https://sdaconsulting.az/uploads/filename.jpg"
echo "NOT: https://sdaconsulting.az/uploads/uploads/filename.jpg"
