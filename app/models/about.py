from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin

class About(Base, TimestampMixin):
    __tablename__ = "about"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    experience: Mapped[str] = mapped_column(Text, nullable=False)
    project_count: Mapped[str] = mapped_column(Text, nullable=False)
    members: Mapped[str] = mapped_column(Text, nullable=False)
    
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
