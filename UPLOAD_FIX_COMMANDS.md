# SDA Upload Fix Commands
# Run these commands on your production server

# 1. Go to the sda directory
cd ~/sda

# 2. Create uploads directory on host
mkdir -p uploads

# 3. Copy all files from container to host
docker exec sda_web_1 find /app/uploads -type f 2>/dev/null | while read file; do
    rel_path=${file#/app/uploads/}
    echo "Copying: $rel_path"
    mkdir -p "uploads/$(dirname "$rel_path")" 2>/dev/null
    docker cp sda_web_1:$file uploads/$rel_path 2>/dev/null
done

# 4. Restart services to apply volume changes
docker-compose down
docker-compose up -d

# 5. Wait for services to start
sleep 15

# 6. Verify the fix
echo "Checking if file is now accessible on host:"
ls -la uploads/4613a2ee-dde0-480a-9312-e6088de6edf3.jpeg

# 7. Test the URL
curl -I https://sdaconsulting.az/uploads/4613a2ee-dde0-480a-9312-e6088de6edf3.jpeg
