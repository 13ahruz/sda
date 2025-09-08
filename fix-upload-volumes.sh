#!/bin/bash

# Complete Upload Debug and Fix Script
echo "=== SDA Upload Debug and Fix ==="

cd ~/sda

echo "Step 1: Checking current setup..."
echo "Docker containers:"
docker ps | grep sda

echo ""
echo "Step 2: Checking Docker volume mounts..."
echo "Checking if uploads directory is properly mounted:"
docker inspect sda_web_1 | grep -A 10 -B 5 "Mounts" 2>/dev/null || echo "Cannot inspect container"

echo ""
echo "Step 3: Checking uploads directory..."
echo "Host uploads directory:"
ls -la uploads/

echo "Container uploads directory:"
docker exec sda_web_1 ls -la /app/ 2>/dev/null | grep uploads || echo "No uploads in container /app/"
docker exec sda_web_1 ls -la /app/uploads/ 2>/dev/null || echo "Container uploads directory not accessible"

echo ""
echo "Step 4: Checking docker-compose volume configuration..."
echo "Volume configuration in docker-compose.yml:"
grep -A 5 -B 5 "uploads" docker-compose.yml 2>/dev/null || echo "No volume config found"

echo ""
echo "Step 5: Creating proper volume mount if missing..."
echo "Stopping container..."
docker-compose stop web

echo "Checking docker-compose.yml for volume configuration..."
if ! grep -q "uploads.*uploads" docker-compose.yml 2>/dev/null; then
    echo "Adding uploads volume mount to docker-compose.yml..."
    
    # Create backup
    cp docker-compose.yml docker-compose.yml.backup
    
    # Add volume mount if it doesn't exist
    if grep -q "volumes:" docker-compose.yml; then
        echo "Volume section exists, checking for uploads mount..."
        if ! grep -q "./uploads:/app/uploads" docker-compose.yml; then
            sed -i '/volumes:/a\      - ./uploads:/app/uploads' docker-compose.yml
            echo "Added uploads volume mount"
        fi
    else
        echo "Need to add entire volumes section"
        # This is more complex - let's check the actual file structure
    fi
fi

echo ""
echo "Step 6: Ensuring uploads directory exists with correct permissions..."
mkdir -p uploads
chmod 755 uploads
chown -R 1000:1000 uploads 2>/dev/null || echo "Cannot change ownership (may need sudo)"

echo ""
echo "Step 7: Restarting container..."
docker-compose up -d web

echo "Waiting for container to start..."
sleep 10

echo ""
echo "Step 8: Testing upload endpoint..."
echo "Container logs:"
docker logs sda_web_1 --tail 10

echo ""
echo "Testing API:"
curl -s http://localhost:8000/ && echo "API is responding"

echo ""
echo "=== Manual Test Instructions ==="
echo "1. Try uploading an image in the admin panel"
echo "2. Check these locations for the file:"
echo "   - Host: ~/sda/uploads/"
echo "   - Container: docker exec sda_web_1 ls -la /app/uploads/"
echo "3. Check the logs for debug output:"
echo "   docker logs sda_web_1 --tail 20"
