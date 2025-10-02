#!/usr/bin/env python3
"""
Script to populate the database with sample projects
"""
import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings
from app.models.projects import Project
from app.models.property_sectors import PropertySector

async def populate_projects():
    database_url = settings.DATABASE_URL or f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if we already have projects
        existing_projects = session.query(Project).count()
        if existing_projects > 0:
            print(f"Database already has {existing_projects} projects. Skipping population.")
            return
        
        # Create property sector if not exists
        shopping_mall_sector = session.query(PropertySector).filter_by(title="Shopping Mall").first()
        if not shopping_mall_sector:
            shopping_mall_sector = PropertySector(
                title="Shopping Mall",
                description="Commercial shopping centers and retail complexes"
            )
            session.add(shopping_mall_sector)
            session.commit()
            session.refresh(shopping_mall_sector)
        
        # Sample projects data (only using fields that exist in the model)
        projects_data = [
            {
                "title": "Sevinc Mall",
                "tag": "sevinc-mall", 
                "cover_photo_url": "/assets/images/sevincmall.png",
                "year": 2024,
                "client": "Sevinc Mall Development",
                "property_sector_id": shopping_mall_sector.id
            },
            {
                "title": "Podium Mall", 
                "tag": "podium-mall",
                "cover_photo_url": "/assets/images/podiummall.png", 
                "year": 2023,
                "client": "Podium Mall Holdings",
                "property_sector_id": shopping_mall_sector.id
            },
            {
                "title": "Greenville Mall",
                "tag": "greenville-mall", 
                "cover_photo_url": "/assets/images/greenville.png",
                "year": 2024,
                "client": "Greenville Properties", 
                "property_sector_id": shopping_mall_sector.id
            }
        ]
        
        # Create projects
        for project_data in projects_data:
            project = Project(**project_data)
            session.add(project)
        
        session.commit()
        print(f"Successfully created {len(projects_data)} projects!")
        
        # Verify creation
        total_projects = session.query(Project).count()
        print(f"Total projects in database: {total_projects}")
        
    except Exception as e:
        session.rollback()
        print(f"Error populating projects: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    asyncio.run(populate_projects())