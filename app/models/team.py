from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin

class TeamMember(Base, TimestampMixin):
    __tablename__ = "team_members"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Multilingual name fields
    full_name_en: Mapped[str | None] = mapped_column(Text)
    full_name_az: Mapped[str | None] = mapped_column(Text)
    full_name_ru: Mapped[str | None] = mapped_column(Text)
    
    # Multilingual role fields
    role_en: Mapped[str | None] = mapped_column(Text)
    role_az: Mapped[str | None] = mapped_column(Text)
    role_ru: Mapped[str | None] = mapped_column(Text)
    
    # Legacy fields
    full_name: Mapped[str | None] = mapped_column(Text)
    role: Mapped[str | None] = mapped_column(Text)
    
    photo_url: Mapped[str | None] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    __table_args__ = (
        Index("ix_team_members_full_name", "full_name"),
        Index("ix_team_members_order", "order"),
    )

class TeamSection(Base, TimestampMixin):
    __tablename__ = "team_sections"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    button_text: Mapped[str | None] = mapped_column(Text)
    
    items: Mapped[list["TeamSectionItem"]] = relationship(back_populates="section", cascade="all, delete-orphan", lazy="select")

class TeamSectionItem(Base, TimestampMixin):
    __tablename__ = "team_section_items"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_section_id: Mapped[int] = mapped_column(ForeignKey("team_sections.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    photo_url: Mapped[str | None] = mapped_column(Text)
    button_text: Mapped[str | None] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    section: Mapped[TeamSection] = relationship(back_populates="items")
    
    __table_args__ = (
        Index("ix_team_section_items_section_order", "team_section_id", "order"),
    )
