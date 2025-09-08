from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi_cache import FastAPICache
from .core.config import settings
from .core.cache import init_cache
from .routers import (
    services,
    approaches,
    property_sectors,
    projects,
    news,
    partners,
    team,
    contact,
    about,
    work_process,
    uploads
)

# Create uploads directory structure if it doesn't exist
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

# Create subdirectories for organized file storage
subdirs = [
    "projects/covers",
    "projects/photos", 
    "team/members",
    "team/sections",
    "about/photos",
    "about/logos",
    "services/icons",
    "partners/logos",
    "work-processes"
]

for subdir in subdirs:
    (UPLOADS_DIR / subdir).mkdir(parents=True, exist_ok=True)

# Create resources directory if it doesn't exist
RESOURCES_DIR = Path("resources")
RESOURCES_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(services.router, prefix=settings.API_V1_STR, tags=["services"])
app.include_router(approaches.router, prefix=settings.API_V1_STR, tags=["approaches"])
app.include_router(property_sectors.router, prefix=settings.API_V1_STR, tags=["property sectors"])
app.include_router(projects.router, prefix=settings.API_V1_STR, tags=["projects"])
app.include_router(news.router, prefix=settings.API_V1_STR, tags=["news"])
app.include_router(partners.router, prefix=settings.API_V1_STR, tags=["partners"])
app.include_router(team.router, prefix=settings.API_V1_STR, tags=["team"])
app.include_router(contact.router, prefix=settings.API_V1_STR, tags=["contact"])
app.include_router(about.router, prefix=settings.API_V1_STR, tags=["about"])
app.include_router(work_process.router, prefix=settings.API_V1_STR, tags=["work processes"])

# Mount static file servers
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/resources", StaticFiles(directory="resources"), name="resources")

@app.on_event("startup")
async def startup_event():
    await init_cache()

# Include uploads router
app.include_router(uploads.router, prefix=settings.API_V1_STR, tags=["uploads"])

@app.get("/")
async def root():
    return {"message": "Welcome to SDA API"}
