from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin

class News(Base, TimestampMixin):
    __tablename__ = "news"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    photo_url: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str]] = mapped_column(ARRAY(Text))
    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    
    sections: Mapped[list["NewsSection"]] = relationship(back_populates="news", cascade="all, delete-orphan", lazy="selectin")
    
    __table_args__ = (
        Index("ix_news_tags", "tags", postgresql_using="gin"),
        Index("ix_news_created_at", "created_at"),
    )

class NewsSection(Base, TimestampMixin):
    __tablename__ = "news_sections"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    news_id: Mapped[int] = mapped_column(ForeignKey("news.id", ondelete="CASCADE"))
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    heading: Mapped[str | None] = mapped_column(Text)
    content: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(Text)
    
    news: Mapped[News] = relationship(back_populates="sections")
    
    __table_args__ = (
        Index("ix_news_sections_news_order", "news_id", "order"),
    )
