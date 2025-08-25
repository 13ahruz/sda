from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin

class Partner(Base, TimestampMixin):
    __tablename__ = "partners"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    button_text: Mapped[str | None] = mapped_column(Text)
    
    logos: Mapped[list["PartnerLogo"]] = relationship(back_populates="partner", cascade="all, delete-orphan", lazy="selectin")

class PartnerLogo(Base, TimestampMixin):
    __tablename__ = "partner_logos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    partner_id: Mapped[int] = mapped_column(ForeignKey("partners.id", ondelete="CASCADE"))
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    partner: Mapped[Partner] = relationship(back_populates="logos")
    
    __table_args__ = (
        Index("ix_partner_logos_partner_order", "partner_id", "order"),
    )
