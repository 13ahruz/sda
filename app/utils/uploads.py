import os
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException, Request
import aiofiles
from pathlib import Path
from ..core.config import settings

# Configuration for file uploads
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {
    "image": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "video": {".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm"},
    "document": {".pdf", ".doc", ".docx", ".txt"},
}

async def upload_file(
    file: UploadFile,
    subdirectory: str = "",
    request: Optional[Request] = None,
    file_type: str = "image"
) -> str:
    """
    Upload a file to the server and return the file URL.
    
    Args:
        file: The uploaded file
        subdirectory: Subdirectory within uploads folder
        file_type: Type of file (image, video, document)
    
    Returns:
        The URL path to the uploaded file
    """
    # Validate file size
    if hasattr(file, 'size') and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // 1024 // 1024}MB"
        )
    
    # Validate file extension
    file_extension = Path(file.filename).suffix.lower()
    allowed_extensions = ALLOWED_EXTENSIONS.get(file_type, ALLOWED_EXTENSIONS["image"])
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed extensions: {', '.join(allowed_extensions)}"
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Create upload directory if it doesn't exist
    upload_path = Path(UPLOAD_DIR) / subdirectory
    upload_path.mkdir(parents=True, exist_ok=True)
    
    # Full file path
    file_path = upload_path / unique_filename
    
    try:
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Generate proper URL based on environment
        if request:
            # Use the request's base URL (this will work with your domain)
            base_url = f"{request.url.scheme}://{request.headers.get('host', request.url.netloc)}"
            print(f"[DEBUG] Using request base URL: {base_url}")
        elif settings.ENVIRONMENT == "production":
            # Use the production domain URL
            base_url = settings.DOMAIN_URL
            print(f"[DEBUG] Using production domain: {base_url}")
        else:
            # Fallback to settings (for development)
            base_url = f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}"
            print(f"[DEBUG] Using development URL: {base_url}")
        
        # Return full URL
        if subdirectory:
            relative_path = f"/{UPLOAD_DIR}/{subdirectory}/{unique_filename}"
        else:
            relative_path = f"/{UPLOAD_DIR}/{unique_filename}"
        final_url = f"{base_url}{relative_path}"
        print(f"[DEBUG] Subdirectory: '{subdirectory}'")
        print(f"[DEBUG] Relative path: {relative_path}")
        print(f"[DEBUG] Final upload URL: {final_url}")
        return final_url
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )

async def delete_file(file_url: str) -> bool:
    """
    Delete a file from the server.
    
    Args:
        file_url: The URL path of the file to delete
    
    Returns:
        True if file was deleted, False if file didn't exist
    """
    try:
        # Convert URL path to file path
        if file_url.startswith('/'):
            file_url = file_url[1:]  # Remove leading slash
        
        file_path = Path(file_url)
        
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    
    except Exception:
        return False

def get_file_info(file_url: str) -> Optional[dict]:
    """
    Get information about an uploaded file.
    
    Args:
        file_url: The URL path of the file
    
    Returns:
        Dictionary with file info or None if file doesn't exist
    """
    try:
        # Convert URL path to file path
        if file_url.startswith('/'):
            file_url = file_url[1:]  # Remove leading slash
        
        file_path = Path(file_url)
        
        if file_path.exists():
            stat = file_path.stat()
            return {
                "name": file_path.name,
                "size": stat.st_size,
                "extension": file_path.suffix,
                "created_at": stat.st_ctime,
                "modified_at": stat.st_mtime,
            }
        return None
    
    except Exception:
        return None

# Legacy compatibility functions
RESOURCES_PATH = Path("resources")

def create_resources_dir():
    """Create resources directory if it doesn't exist"""
    if not RESOURCES_PATH.exists():
        RESOURCES_PATH.mkdir(parents=True)

async def save_upload_file(file: UploadFile, request: Optional[Request] = None) -> Optional[str]:
    """Legacy function - use upload_file instead"""
    try:
        file_url = await upload_file(file, "legacy", request)
        return file_url.replace("/uploads/legacy/", str(RESOURCES_PATH) + "/")
    except:
        return None

def get_file_url(file_path: str, request: Optional[Request] = None) -> str:
    """Convert file path to URL"""
    if request:
        base_url = f"{request.url.scheme}://{request.headers.get('host', request.url.netloc)}"
        return f"{base_url}/resources/{os.path.basename(file_path)}"
    elif settings.ENVIRONMENT == "production":
        # Use the production domain URL
        return f"{settings.DOMAIN_URL}/resources/{os.path.basename(file_path)}"
    else:
        # For development, use server host and port
        return f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/resources/{os.path.basename(file_path)}"
