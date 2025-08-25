from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from ..utils.uploads import save_upload_file, get_file_url, RESOURCES_PATH

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile):
    """Upload a file and return its URL"""
    file_path = await save_upload_file(file)
    if not file_path:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only images (JPEG, PNG, GIF, WebP) and videos (MP4, MPEG, MOV) are allowed."
        )
    return {"url": get_file_url(file_path)}

@router.get("/resources/{filename}")
async def get_resource(filename: str):
    """Serve a file from the resources directory"""
    file_path = RESOURCES_PATH / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
