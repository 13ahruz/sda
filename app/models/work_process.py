from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, TimestampMixin

class WorkProcess(Base, TimestampMixin):
    __tablename__ = "work_processes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Multilingual title fields
    title_en: Mapped[str | None] = mapped_column(Text)
    title_az: Mapped[str | None] = mapped_column(Text)
    title_ru: Mapped[str | None] = mapped_column(Text)
    
    # Multilingual description fields
    description_en: Mapped[str | None] = mapped_column(Text)
    description_az: Mapped[str | None] = mapped_column(Text)
    description_ru: Mapped[str | None] = mapped_column(Text)
    
    # Legacy fields
    title: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    image_url: Mapped[str | None] = mapped_column(Text)
    
    __table_args__ = (
        Index("ix_work_processes_order", "order"),
    )
