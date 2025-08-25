from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin

class Service(Base, TimestampMixin):
    __tablename__ = "services"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    icon_url: Mapped[str | None] = mapped_column(Text)
    
    __table_args__ = (
        Index("ix_services_order", "order"),
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
