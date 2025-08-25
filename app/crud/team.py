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
        """Get team members ordered by display order and name"""
        return (
            db.query(self.model)
            .order_by(self.model.display_order.asc(), self.model.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_department(
        self,
        db: Session,
        *,
        department: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[TeamMember]:
        """Get team members by department"""
        return (
            db.query(self.model)
            .filter(self.model.department.ilike(f"%{department}%"))
            .order_by(self.model.display_order.asc(), self.model.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

class CRUDTeamSection(CRUDBase[TeamSection, TeamSectionCreate, TeamSectionUpdate]):
    def get_multi_ordered(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[TeamSection]:
        """Get team sections ordered by display order"""
        return (
            db.query(self.model)
            .order_by(self.model.display_order.asc())
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
