#!/bin/bash

echo "=== Fixing Git Conflict and Applying Volume Mount ==="
cd ~/sda

echo "1. Current git status:"
git status

echo ""
echo "2. Committing local docker-compose.yml changes..."
git add docker-compose.yml
git commit -m "Fix upload volume mounting: ./uploads:/app/uploads"

echo ""
echo "3. Pulling latest changes..."
git pull origin main

echo ""
echo "4. Checking if volume mount is correct in docker-compose.yml..."
echo "Looking for volume mount:"
grep -A 5 -B 5 "uploads" docker-compose.yml

echo ""
echo "5. If volume mount is missing, applying it now..."
if ! grep -q "./uploads:/app/uploads" docker-compose.yml; then
    echo "Volume mount missing, adding it..."
    
    # Backup
    cp docker-compose.yml docker-compose.yml.backup-$(date +%s)
    
    # Add the correct volume mount
    sed -i '/- \.\/:/a\      - ./uploads:/app/uploads' docker-compose.yml
    
    echo "Added volume mount to docker-compose.yml"
else
    echo "Volume mount already exists"
fi

echo ""
echo "6. Ensuring uploads directory exists with correct permissions..."
mkdir -p uploads
chmod 755 uploads

echo ""
echo "7. Stopping and rebuilding containers with proper volume..."
docker-compose down
docker-compose up -d --build

echo ""
echo "8. Waiting for services to start..."
sleep 20

echo ""
echo "9. Checking if volume mount is working..."
echo "Files in host uploads directory:"
ls -la uploads/

echo ""
echo "Files in container uploads directory:"
docker exec sda_web_1 ls -la /app/uploads/ 2>/dev/null || echo "Cannot access container uploads"

echo ""
echo "10. Testing new file creation..."
echo "Creating test file in host uploads:"
echo "test" > uploads/test-volume-mount.txt

echo "Checking if file appears in container:"
docker exec sda_web_1 ls -la /app/uploads/test-volume-mount.txt 2>/dev/null && echo "✅ Volume mount working!" || echo "❌ Volume mount not working"

echo ""
echo "11. Testing URL accessibility..."
if [ -f "uploads/1c2dfdb8-ce6f-42e6-9749-e7192b275c4d.jpeg" ]; then
    echo "✅ New file exists on host"
    curl -I https://sdaconsulting.az/uploads/1c2dfdb8-ce6f-42e6-9749-e7192b275c4d.jpeg
else
    echo "❌ New file not found on host, checking container..."
    docker exec sda_web_1 find /app/uploads -name "*1c2dfdb8*" -type f
fi

echo ""
echo "=== Fix Complete ==="
