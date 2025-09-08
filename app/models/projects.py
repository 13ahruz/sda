from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin
from .property_sectors import PropertySector

class Project(Base, TimestampMixin):
    __tablename__ = "projects"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    tag: Mapped[str | None] = mapped_column(Text)
    client: Mapped[str | None] = mapped_column(Text)
    year: Mapped[int | None] = mapped_column(Integer)
    property_sector_id: Mapped[int | None] = mapped_column(ForeignKey("property_sectors.id", ondelete="SET NULL"))
    cover_photo_url: Mapped[str | None] = mapped_column(Text)
    
    photos: Mapped[list["ProjectPhoto"]] = relationship(back_populates="project", cascade="all, delete-orphan", lazy="select")
    property_sector: Mapped[PropertySector] = relationship(lazy="select")
    
    __table_args__ = (
        Index("ix_projects_property_sector", "property_sector_id"),
        Index("ix_projects_year", "year"),
        Index("ix_projects_tag", "tag"),
    )

class ProjectPhoto(Base, TimestampMixin):
    __tablename__ = "project_photos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    project: Mapped[Project] = relationship(back_populates="photos")
    
    __table_args__ = (
        Index("ix_project_photos_project_order", "project_id", "order"),
    )
