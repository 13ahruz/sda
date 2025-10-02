"""Add slug fields and frontend compatibility

Revision ID: frontend_compat_2025
Revises: ea7a667484f5
Create Date: 2025-10-02 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'frontend_compat_2025'
down_revision: Union[str, None] = 'add_image_fields'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### Add slug field to services table ###
    op.add_column('services', sa.Column('slug', sa.Text(), nullable=True))
    op.add_column('services', sa.Column('hero_text', sa.Text(), nullable=True))
    op.add_column('services', sa.Column('image_url', sa.Text(), nullable=True))
    op.add_column('services', sa.Column('meta_title', sa.Text(), nullable=True))
    op.add_column('services', sa.Column('meta_description', sa.Text(), nullable=True))
    op.create_index('ix_services_slug', 'services', ['slug'], unique=True)
    
    # ### Add slug and other fields to news table ###
    op.add_column('news', sa.Column('slug', sa.Text(), nullable=True))
    op.add_column('news', sa.Column('category', sa.Text(), nullable=True))
    op.add_column('news', sa.Column('excerpt', sa.Text(), nullable=True))
    op.add_column('news', sa.Column('content', sa.Text(), nullable=True))
    op.add_column('news', sa.Column('date', sa.Date(), nullable=True))
    op.add_column('news', sa.Column('author', sa.Text(), nullable=True))
    op.add_column('news', sa.Column('read_time', sa.Text(), nullable=True))
    op.add_column('news', sa.Column('order', sa.Integer(), nullable=False, server_default='0'))
    op.create_index('ix_news_slug', 'news', ['slug'], unique=True)
    op.create_index('ix_news_order', 'news', ['order'], unique=False)
    op.create_index('ix_news_category', 'news', ['category'], unique=False)
    
    # ### Add order field to team_members table ###
    op.add_column('team_members', sa.Column('order', sa.Integer(), nullable=False, server_default='0'))
    op.create_index('ix_team_members_order', 'team_members', ['order'], unique=False)
    
    # ### Add additional project fields ###
    op.add_column('projects', sa.Column('slug', sa.Text(), nullable=True))
    op.add_column('projects', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('projects', sa.Column('services', postgresql.ARRAY(sa.Text()), nullable=True))
    op.add_column('projects', sa.Column('order', sa.Integer(), nullable=False, server_default='0'))
    op.create_index('ix_projects_slug', 'projects', ['slug'], unique=True)
    op.create_index('ix_projects_order', 'projects', ['order'], unique=False)
    
    # ### Update existing data with default slug values ###
    # Generate slugs for existing services
    op.execute("""
        UPDATE services 
        SET slug = CASE 
            WHEN LOWER(name) LIKE '%development%' THEN 'property-development'
            WHEN LOWER(name) LIKE '%leasing%' OR LOWER(name) LIKE '%sales%' THEN 'leasing-sales'
            WHEN LOWER(name) LIKE '%research%' OR LOWER(name) LIKE '%analytics%' THEN 'market-research'
            WHEN LOWER(name) LIKE '%marketing%' OR LOWER(name) LIKE '%strategy%' THEN 'marketing-strategy'
            ELSE LOWER(REPLACE(REPLACE(name, ' ', '-'), '&', 'and'))
        END
        WHERE slug IS NULL;
    """)
    
    # Generate slugs for existing news
    op.execute("""
        UPDATE news 
        SET slug = LOWER(REPLACE(REPLACE(REPLACE(title, ' ', '-'), '&', 'and'), '?', ''))
        WHERE slug IS NULL;
    """)
    
    # Generate slugs for existing projects
    op.execute("""
        UPDATE projects 
        SET slug = LOWER(REPLACE(REPLACE(title, ' ', '-'), '&', 'and'))
        WHERE slug IS NULL;
    """)
    
    # Set default categories for news
    op.execute("""
        UPDATE news 
        SET category = CASE 
            WHEN tags::text LIKE '%trend%' THEN 'Trends'
            WHEN tags::text LIKE '%insight%' THEN 'Insights'
            WHEN tags::text LIKE '%guide%' THEN 'Guides'
            ELSE 'Insights'
        END
        WHERE category IS NULL;
    """)


def downgrade() -> None:
    # ### Remove added indexes ###
    op.drop_index('ix_projects_order', table_name='projects')
    op.drop_index('ix_projects_slug', table_name='projects')
    op.drop_index('ix_team_members_order', table_name='team_members')
    op.drop_index('ix_news_category', table_name='news')
    op.drop_index('ix_news_order', table_name='news')
    op.drop_index('ix_news_slug', table_name='news')
    op.drop_index('ix_services_slug', table_name='services')
    
    # ### Remove added columns ###
    op.drop_column('projects', 'order')
    op.drop_column('projects', 'services')
    op.drop_column('projects', 'description')
    op.drop_column('projects', 'slug')
    op.drop_column('team_members', 'order')
    op.drop_column('news', 'order')
    op.drop_column('news', 'read_time')
    op.drop_column('news', 'author')
    op.drop_column('news', 'date')
    op.drop_column('news', 'content')
    op.drop_column('news', 'excerpt')
    op.drop_column('news', 'category')
    op.drop_column('news', 'slug')
    op.drop_column('services', 'meta_description')
    op.drop_column('services', 'meta_title')
    op.drop_column('services', 'image_url')
    op.drop_column('services', 'hero_text')
    op.drop_column('services', 'slug')