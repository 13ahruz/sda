from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin

class Service(Base, TimestampMixin):
    __tablename__ = "services"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Multilingual name/title fields
    name_en: Mapped[str | None] = mapped_column(Text)
    name_az: Mapped[str | None] = mapped_column(Text)
    name_ru: Mapped[str | None] = mapped_column(Text)
    
    # Multilingual description fields
    description_en: Mapped[str | None] = mapped_column(Text)
    description_az: Mapped[str | None] = mapped_column(Text)
    description_ru: Mapped[str | None] = mapped_column(Text)
    
    # Multilingual hero text fields
    hero_text_en: Mapped[str | None] = mapped_column(Text)
    hero_text_az: Mapped[str | None] = mapped_column(Text)
    hero_text_ru: Mapped[str | None] = mapped_column(Text)
    
    # Multilingual meta fields
    meta_title_en: Mapped[str | None] = mapped_column(Text)
    meta_title_az: Mapped[str | None] = mapped_column(Text)
    meta_title_ru: Mapped[str | None] = mapped_column(Text)
    
    meta_description_en: Mapped[str | None] = mapped_column(Text)
    meta_description_az: Mapped[str | None] = mapped_column(Text)
    meta_description_ru: Mapped[str | None] = mapped_column(Text)
    
    # Legacy fields (will be migrated to _en versions)
    name: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    hero_text: Mapped[str | None] = mapped_column(Text)
    meta_title: Mapped[str | None] = mapped_column(Text)
    meta_description: Mapped[str | None] = mapped_column(Text)
    
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    image_url: Mapped[str | None] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    icon_url: Mapped[str | None] = mapped_column(Text)
    
    __table_args__ = (
        Index("ix_services_order", "order"),
        Index("ix_services_slug", "slug"),
    )

class ServiceBenefit(Base, TimestampMixin):
    __tablename__ = "service_benefits"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    __table_args__ = (
        Index("ix_service_benefits_order", "order"),
    )
