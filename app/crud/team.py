from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..crud.base import CRUDBase
from ..models.team import TeamMember, TeamSection, TeamSectionItem
from ..schemas.team import (
    TeamMemberCreate,
    TeamMemberUpdate,
    TeamSectionCreate,
    TeamSectionUpdate,
    TeamSectionItemCreate,
    TeamSectionItemUpdate
)

class CRUDTeamMember(CRUDBase[TeamMember, TeamMemberCreate, TeamMemberUpdate]):
    def get_multi_ordered(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[TeamMember]:
        """Get team members ordered by full_name"""
        return (
            db.query(self.model)
            .order_by(self.model.full_name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_role(
        self,
        db: Session,
        *,
        role: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[TeamMember]:
        """Get team members by role"""
        return (
            db.query(self.model)
            .filter(self.model.role.ilike(f"%{role}%"))
            .order_by(self.model.full_name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

class CRUDTeamSection(CRUDBase[TeamSection, TeamSectionCreate, TeamSectionUpdate]):
    def create(self, db: Session, *, obj_in: TeamSectionCreate) -> TeamSection:
        # Extract items data before creating the team section
        obj_in_data = obj_in.model_dump()
        items_data = obj_in_data.pop('items', [])
        
        # Create the team section without items
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Add items if any
        if items_data:
            for item_data in items_data:
                item_obj = TeamSectionItem(team_section_id=db_obj.id, **item_data)
                db.add(item_obj)
            db.commit()
            db.refresh(db_obj)
        
        return db_obj

    def get_multi_ordered(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[TeamSection]:
        """Get team sections ordered by title"""
        return (
            db.query(self.model)
            .order_by(self.model.title.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

class CRUDTeamSectionItem(CRUDBase[TeamSectionItem, TeamSectionItemCreate, TeamSectionItemUpdate]):
    def get_by_section(
        self,
        db: Session,
        *,
        section_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TeamSectionItem]:
        """Get team section items by section ID"""
        return (
            db.query(self.model)
            .filter(self.model.team_section_id == section_id)
            .order_by(self.model.display_order.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

team_member = CRUDTeamMember(TeamMember)
team_section = CRUDTeamSection(TeamSection)
team_section_item = CRUDTeamSectionItem(TeamSectionItem)
