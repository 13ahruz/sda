import os
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
import aiofiles
from pathlib import Path

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
        
        # Return URL path (relative to server root)
        return f"/{UPLOAD_DIR}/{subdirectory}/{unique_filename}" if subdirectory else f"/{UPLOAD_DIR}/{unique_filename}"
    
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

async def save_upload_file(file: UploadFile) -> Optional[str]:
    """Legacy function - use upload_file instead"""
    try:
        file_url = await upload_file(file, "legacy")
        return file_url.replace("/uploads/legacy/", str(RESOURCES_PATH) + "/")
    except:
        return None

def get_file_url(file_path: str) -> str:
    """Convert file path to URL"""
    return f"/resources/{os.path.basename(file_path)}"
