#!/bin/bash

# Debug Upload File Location Script
echo "Debugging file upload location..."

cd ~/sda

echo "=== Searching for the uploaded file ==="
FILE_ID="4613a2ee-dde0-480a-9312-e6088de6edf3"
echo "Looking for file: $FILE_ID"

echo ""
echo "Searching entire uploads directory:"
find uploads -name "*$FILE_ID*" -type f 2>/dev/null || echo "File not found in uploads directory"

echo ""
echo "Searching entire sda directory:"
find . -name "*$FILE_ID*" -type f 2>/dev/null || echo "File not found in sda directory"

echo ""
echo "=== Checking upload directory structure ==="
echo "Current uploads directory structure:"
find uploads -type d | sort

echo ""
echo "Files in uploads root:"
ls -la uploads/ 2>/dev/null || echo "uploads directory not found"

echo ""
echo "=== Checking container logs for upload ==="
echo "Recent backend logs (looking for upload activity):"
docker logs sda_web_1 --tail 30 2>/dev/null | grep -E "(DEBUG|upload|4613a2ee)" || echo "No relevant logs found"

echo ""
echo "=== Checking upload permissions ==="
echo "Upload directory permissions:"
ls -la uploads/ 2>/dev/null

echo ""
echo "=== Testing upload endpoint directly ==="
echo "Testing if upload endpoint is working:"
curl -s http://localhost:8000/api/v1/upload -X POST \
  -F "file=@/dev/null" 2>/dev/null || echo "Upload endpoint not accessible"

echo ""
echo "=== Container information ==="
echo "Backend container status:"
docker ps | grep sda_web

echo ""
echo "Container filesystem - uploads directory:"
docker exec sda_web_1 ls -la /app/uploads 2>/dev/null || echo "Cannot access container uploads directory"
