from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from ..utils.uploads import upload_file, UPLOAD_DIR

router = APIRouter()

@router.post("/upload")
async def upload_file_endpoint(file: UploadFile):
    """Upload a file and return its URL"""
    try:
        # Determine subdirectory based on file type/content
        subdirectory = "images"  # Default to images
        if file.content_type and file.content_type.startswith('video/'):
            subdirectory = "videos"
        
        file_url = await upload_file(file, subdirectory, "image")
        return {"url": file_url}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )

@router.get("/uploads/{path:path}")
async def get_uploaded_file(path: str):
    """Serve a file from the uploads directory"""
    file_path = Path(UPLOAD_DIR) / path
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
