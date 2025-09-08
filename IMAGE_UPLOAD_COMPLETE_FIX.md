# SDA Image Upload Fix - Complete Solution

## Issue Summary
The admin panel was failing to upload images with the error:
```
"Failed to upload file: 'str' object has no attribute 'url'"
```

## Root Cause
1. The FastAPI upload endpoint was calling functions that expected a `request` parameter
2. The environment was set to "development" instead of "production"
3. URL generation was failing when request parameter was missing

## Files Fixed

### 1. `app/routers/uploads.py`
- Fixed the `/upload` endpoint to work without requiring request parameter
- Updated imports and error handling

### 2. `app/utils/uploads.py`
- Fixed upload_file function parameter handling
- Added production URL generation fallback
- Added debug logging for troubleshooting

### 3. `app/core/config.py`
- Set default environment to "production"
- Configured proper domain URL

### 4. `app/routers/about.py` and `app/routers/team.py`
- Fixed missing Request imports
- Updated function signatures

## Deployment Instructions

### On your production server (srv701472):

1. **Copy the fixed files to your server:**
   ```bash
   # From your local machine, upload the fixed sda folder
   scp -r sda/ root@srv701472:~/
   ```

2. **Run the complete fix script:**
   ```bash
   cd ~/sda
   chmod +x complete-image-fix.sh
   ./complete-image-fix.sh
   ```

3. **Manually apply the fix if needed:**
   ```bash
   cd ~/sda
   
   # Set environment variables
   echo "ENVIRONMENT=production" >> .env
   echo "DOMAIN_URL=https://sdaconsulting.az" >> .env
   
   # Rebuild containers
   docker-compose down
   docker rmi sda_web 2>/dev/null || true
   docker-compose up -d --build
   
   # Wait and check
   sleep 15
   docker ps
   docker logs sda_web_1 --tail 20
   ```

## Testing the Fix

### 1. Test API directly:
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test-image.jpg"
```

Expected response:
```json
{"url": "https://sdaconsulting.az/uploads/test-filename.jpg"}
```

### 2. Test from admin panel:
1. Go to your admin panel: `http://your-server:8001/admin`
2. Create a new project
3. Upload a cover photo
4. Upload project photos
5. Check that the URLs are properly saved and images are accessible

### 3. Verify images are accessible:
- Check that uploaded images are accessible at: `https://sdaconsulting.az/uploads/...`
- Images should load properly in your frontend

## Expected Behavior After Fix

1. **Admin Panel Upload**: Should successfully upload images and return proper URLs
2. **URL Format**: URLs should be `https://sdaconsulting.az/uploads/...`
3. **Image Access**: Images should be accessible from your domain via nginx proxy
4. **No Errors**: No more "Connection refused" or "'str' object has no attribute 'url'" errors

## Debug Information

If you still see issues, check the debug logs for:
```
[DEBUG] Using production domain: https://sdaconsulting.az
[DEBUG] Final upload URL: https://sdaconsulting.az/uploads/...
```

This confirms the URL generation is working correctly.

## Troubleshooting

### If containers won't start:
```bash
docker logs sda_web_1
```

### If upload still fails:
```bash
# Check if backend is responding
curl http://localhost:8000/

# Check upload endpoint directly
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@test.jpg"
```

### If images not accessible via domain:
- Check nginx configuration
- Verify nginx is running: `sudo systemctl status nginx`
- Check nginx logs: `sudo tail -f /var/log/nginx/error.log`

The fix should resolve all image upload issues in your admin panel!
