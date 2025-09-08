# Git Conflict Resolution and Volume Fix Commands
# Run these commands on your production server

cd ~/sda

# 1. Commit local changes
git add docker-compose.yml
git commit -m "Fix upload volume mounting"

# 2. Pull and merge latest changes
git pull origin main

# 3. Check current docker-compose.yml volume configuration
echo "Current volume configuration:"
grep -A 10 -B 5 "volumes:" docker-compose.yml

# 4. Add volume mount if missing
if ! grep -q "./uploads:/app/uploads" docker-compose.yml; then
    echo "Adding uploads volume mount..."
    cp docker-compose.yml docker-compose.yml.backup
    sed -i '/- \.:/a\      - ./uploads:/app/uploads' docker-compose.yml
    echo "Volume mount added"
fi

# 5. Apply the volume fix
docker-compose down
docker-compose up -d

# 6. Wait and test
sleep 20

# 7. Create test file to verify volume mount
echo "test" > uploads/test-volume.txt
docker exec sda_web_1 ls -la /app/uploads/test-volume.txt

# 8. Check if new upload file exists on host
ls -la uploads/1c2dfdb8-ce6f-42e6-9749-e7192b275c4d.jpeg

# 9. Test URL
curl -I https://sdaconsulting.az/uploads/1c2dfdb8-ce6f-42e6-9749-e7192b275c4d.jpeg
