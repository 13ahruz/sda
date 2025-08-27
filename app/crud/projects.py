from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, and_
from ..crud.base import CRUDBase
from ..models.projects import Project, ProjectPhoto
from ..schemas.projects import ProjectCreate, ProjectUpdate, ProjectPhotoCreate, ProjectPhotoUpdate

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def create(self, db: Session, *, obj_in: ProjectCreate) -> Project:
        # Extract photos data before creating the project
        obj_in_data = obj_in.model_dump()
        photos_data = obj_in_data.pop('photos', [])
        
        # Create the project without photos
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Add photos if any
        if photos_data:
            for photo_data in photos_data:
                photo_obj = ProjectPhoto(project_id=db_obj.id, **photo_data)
                db.add(photo_obj)
            db.commit()
            db.refresh(db_obj)
        
        return db_obj

    def get_multi_filtered(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        property_sector_id: Optional[int] = None,
        year: Optional[int] = None,
        tag: Optional[str] = None
    ) -> List[Project]:
        query = db.query(self.model)
        
        if property_sector_id is not None:
            query = query.filter(self.model.property_sector_id == property_sector_id)
        if year is not None:
            query = query.filter(self.model.year == year)
        if tag is not None:
            query = query.filter(self.model.tag.ilike(f"%{tag}%"))
            
        return (
            query
            .order_by(desc(self.model.year), asc(self.model.id))
            .offset(skip)
            .limit(limit)
            .all()
        )

class CRUDProjectPhoto(CRUDBase[ProjectPhoto, ProjectPhotoCreate, ProjectPhotoUpdate]):
    def get_by_project(
        self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100
    ) -> List[ProjectPhoto]:
        return (
            db.query(self.model)
            .filter(self.model.project_id == project_id)
            .order_by(asc(self.model.order), asc(self.model.id))
            .offset(skip)
            .limit(limit)
            .all()
        )

project = CRUDProject(Project)
project_photo = CRUDProjectPhoto(ProjectPhoto)
