# SDA Image Upload Fix - Production Deployment Guide

## Issues Fixed

1. **CORS Configuration**: Added `sdaconsulting.az` to allowed origins
2. **Image URL Generation**: Fixed to use proper domain URLs instead of hardcoded IPs
3. **Upload Function Parameters**: Fixed missing `request` parameters in various routers
4. **Environment Configuration**: Added production environment variables
5. **Directory Structure**: Ensured proper uploads directory structure

## Deployment Steps

### 1. On Your Production Server

Copy the updated files to your server and run:

```bash
cd /path/to/your/sda/folder
chmod +x deploy-production.sh
./deploy-production.sh
```

### 2. Set Environment Variables

Create or update your `.env` file with:

```bash
ENVIRONMENT=production
DOMAIN_URL=https://sdaconsulting.az
```

### 3. Restart Your Backend Service

```bash
# If using systemd
sudo systemctl restart sda-backend

# If using PM2
pm2 restart sda-backend

# If running manually
pkill -f "uvicorn"
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 &
```

### 4. Verify Nginx Configuration

Your nginx config looks correct, but ensure these locations are properly configured:

```nginx
# Backend API (already configured)
location /api/ {
    proxy_pass http://127.0.0.1:8000;
    # ... your existing headers
}

# Uploads (already configured)
location /uploads/ {
    proxy_pass http://127.0.0.1:8000/uploads/;
    # ... your existing headers
}
```

### 5. Test Image Upload

1. Test upload via API: `POST /api/v1/upload`
2. Check if images are accessible: `https://sdaconsulting.az/uploads/[path]`
3. Verify database URLs are using the correct domain

## Troubleshooting

### Issue: Images still not loading

1. **Check file permissions**:
   ```bash
   ls -la uploads/
   # Should show 755 permissions
   ```

2. **Verify backend is serving files**:
   ```bash
   curl http://127.0.0.1:8000/uploads/test.jpg
   ```

3. **Check nginx logs**:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   sudo tail -f /var/log/nginx/access.log
   ```

### Issue: CORS errors

If you see CORS errors in browser console:

1. Verify your domain is in the CORS origins list
2. Restart the backend after changes
3. Check browser developer tools for specific error messages

### Issue: Upload fails

1. Check uploads directory permissions: `chmod -R 755 uploads/`
2. Verify disk space: `df -h`
3. Check backend logs for specific error messages

## File Structure After Fix

```
sda/
├── uploads/
│   ├── projects/
│   │   ├── covers/
│   │   └── photos/
│   ├── team/
│   │   ├── members/
│   │   └── sections/
│   ├── about/
│   │   ├── photos/
│   │   └── logos/
│   ├── services/
│   │   └── icons/
│   ├── partners/
│   │   └── logos/
│   └── work-processes/
├── resources/
└── app/
    └── ... (your application files)
```

## What Changed

### Backend Files Modified:
- `app/core/config.py` - Added CORS origins and environment config
- `app/utils/uploads.py` - Fixed URL generation and added request parameter
- `app/routers/projects.py` - Already had correct request parameter usage
- `app/routers/about.py` - Added missing request parameter
- `app/routers/team.py` - Added missing request parameter
- `app/main.py` - Added proper directory structure creation

### New Files Created:
- `.env.production` - Production environment configuration
- `deploy-production.sh` - Deployment script
- This guide

## Testing

After deployment, test with:

```bash
# Test API endpoint
curl -X POST "https://sdaconsulting.az/api/v1/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test-image.jpg"

# Should return: {"url": "https://sdaconsulting.az/uploads/..."}
```

The returned URL should be accessible in your browser and work in your frontend application.
