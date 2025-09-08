from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin

class PropertySector(Base, TimestampMixin):
    __tablename__ = "property_sectors"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    inns: Mapped[list["SectorInn"]] = relationship(back_populates="property_sector", cascade="all, delete-orphan", lazy="select")
    projects: Mapped[list["Project"]] = relationship(back_populates="property_sector", lazy="select")
    
    __table_args__ = (
        Index("ix_property_sectors_order", "order"),
    )

class SectorInn(Base, TimestampMixin):
    __tablename__ = "sector_inns"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_sector_id: Mapped[int] = mapped_column(ForeignKey("property_sectors.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    property_sector: Mapped["PropertySector"] = relationship(back_populates="inns")
    
    __table_args__ = (
        UniqueConstraint("property_sector_id", "title", name="uq_sector_inns_sector_title"),
        Index("ix_sector_inns_sector_order", "property_sector_id", "order"),
    )
