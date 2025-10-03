from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin

class News(Base, TimestampMixin):
    __tablename__ = "news"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    
    # Multilingual title fields
    title_en: Mapped[str | None] = mapped_column(Text)
    title_az: Mapped[str | None] = mapped_column(Text)
    title_ru: Mapped[str | None] = mapped_column(Text)
    
    # Multilingual excerpt fields
    excerpt_en: Mapped[str | None] = mapped_column(Text)
    excerpt_az: Mapped[str | None] = mapped_column(Text)
    excerpt_ru: Mapped[str | None] = mapped_column(Text)
    
    # Multilingual content fields
    content_en: Mapped[str | None] = mapped_column(Text)
    content_az: Mapped[str | None] = mapped_column(Text)
    content_ru: Mapped[str | None] = mapped_column(Text)
    
    # Multilingual summary fields
    summary_en: Mapped[str | None] = mapped_column(Text)
    summary_az: Mapped[str | None] = mapped_column(Text)
    summary_ru: Mapped[str | None] = mapped_column(Text)
    
    # Legacy fields (will be migrated to _en versions)
    title: Mapped[str | None] = mapped_column(Text)
    excerpt: Mapped[str | None] = mapped_column(Text)
    content: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)
    
    photo_url: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100))  # Trends, Insights, Guides
    tags: Mapped[list[str]] = mapped_column(ARRAY(Text))
    author: Mapped[str | None] = mapped_column(String(255))
    read_time: Mapped[str | None] = mapped_column(String(50))  # e.g., "5 min read"
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    sections: Mapped[list["NewsSection"]] = relationship(back_populates="news", cascade="all, delete-orphan", lazy="select")
    
    __table_args__ = (
        Index("ix_news_tags", "tags", postgresql_using="gin"),
        Index("ix_news_created_at", "created_at"),
        Index("ix_news_slug", "slug"),
        Index("ix_news_category", "category"),
        Index("ix_news_order", "order"),
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
