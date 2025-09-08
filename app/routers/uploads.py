from fastapi import APIRouter, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse
from pathlib import Path
from ..utils.uploads import upload_file, RESOURCES_PATH

router = APIRouter()

@router.post("/upload")
async def upload_file_endpoint(file: UploadFile):
    """Upload a file and return its URL"""
    try:
        # Use empty subdirectory to avoid double /uploads/ in URL
        file_url = await upload_file(file, "")
        return {"url": file_url}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )

@router.get("/resources/{filename}")
async def get_resource(filename: str):
    """Serve a file from the resources directory"""
    file_path = RESOURCES_PATH / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
