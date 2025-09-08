#!/bin/bash

echo "=== SDA Upload Volume Fix ==="
echo "Fixing Docker volume mounting for uploads directory"
echo ""

cd ~/sda

echo "1. Current situation:"
echo "Files in container:"
docker exec sda_web_1 ls -la /app/uploads/ 2>/dev/null || echo "No container uploads dir"

echo "Files on host:"
ls -la uploads/ 2>/dev/null || echo "No host uploads dir"

echo ""
echo "2. Copying existing files from container to host..."
mkdir -p uploads

# Copy files from container to host
echo "Copying files from container /app/uploads/ to host uploads/..."
docker exec sda_web_1 find /app/uploads -type f 2>/dev/null | while read file; do
    rel_path=${file#/app/uploads/}
    echo "Copying: $rel_path"
    mkdir -p "uploads/$(dirname "$rel_path")" 2>/dev/null
    docker cp sda_web_1:$file uploads/$rel_path 2>/dev/null
done

echo ""
echo "3. Files now on host:"
find uploads/ -type f 2>/dev/null | head -10

echo ""
echo "4. Stopping services..."
docker-compose down

echo ""
echo "5. Starting services with fixed volume..."
docker-compose up -d

echo ""
echo "6. Waiting for services..."
sleep 15

echo ""
echo "7. Verification:"
echo "Container uploads directory:"
docker exec sda_web_1 ls -la /app/uploads/ 2>/dev/null

echo ""
echo "Host uploads directory:"
ls -la uploads/ 2>/dev/null

echo ""
echo "Testing specific file:"
if [ -f "uploads/4613a2ee-dde0-480a-9312-e6088de6edf3.jpeg" ]; then
    echo "✅ File exists on host!"
    ls -la "uploads/4613a2ee-dde0-480a-9312-e6088de6edf3.jpeg"
else
    echo "❌ File still not on host"
fi

echo ""
echo "=== Fix Complete ==="
