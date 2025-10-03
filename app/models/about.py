from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin

class About(Base, TimestampMixin):
    __tablename__ = "about"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Multilingual experience fields
    experience_en: Mapped[str | None] = mapped_column(Text)
    experience_az: Mapped[str | None] = mapped_column(Text)
    experience_ru: Mapped[str | None] = mapped_column(Text)
    
    # Multilingual project count fields
    project_count_en: Mapped[str | None] = mapped_column(Text)
    project_count_az: Mapped[str | None] = mapped_column(Text)
    project_count_ru: Mapped[str | None] = mapped_column(Text)
    
    # Multilingual members fields
    members_en: Mapped[str | None] = mapped_column(Text)
    members_az: Mapped[str | None] = mapped_column(Text)
    members_ru: Mapped[str | None] = mapped_column(Text)
    
    # Legacy fields
    experience: Mapped[str | None] = mapped_column(Text)
    project_count: Mapped[str | None] = mapped_column(Text)
    members: Mapped[str | None] = mapped_column(Text)
    
    logos: Mapped[list["AboutLogo"]] = relationship(back_populates="about", cascade="all, delete-orphan", lazy="select")

class AboutLogo(Base, TimestampMixin):
    __tablename__ = "about_logos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    about_id: Mapped[int] = mapped_column(ForeignKey("about.id", ondelete="CASCADE"))
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    about: Mapped[About] = relationship(back_populates="logos")
    
    __table_args__ = (
        Index("ix_about_logos_about_order", "about_id", "order"),
    )
