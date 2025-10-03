"""
Simple script to populate database with sample multilingual data
"""
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.services import Service
from app.models.projects import Project
from app.models.team import TeamMember
from app.models.property_sectors import PropertySector

def populate_services(db: Session):
    """Populate services with multilingual data"""
    print("Populating services...")
    
    services_data = [
        {
            "name": "Real Estate Development",
            "name_en": "Real Estate Development",
            "name_az": "Daşınmaz Əmlak İnkişafı",
            "name_ru": "Развитие Недвижимости",
            "description": "Comprehensive real estate development services",
            "description_en": "Comprehensive real estate development services",
            "description_az": "Hərtərəfli daşınmaz əmlak inkişaf xidmətləri",
            "description_ru": "Комплексные услуги по развитию недвижимости",
            "slug": "real-estate-development",
            "order": 1
        },
        {
            "name": "Construction Management",
            "name_en": "Construction Management", 
            "name_az": "Tikinti İdarəetməsi",
            "name_ru": "Управление Строительством",
            "description": "Professional construction project management",
            "description_en": "Professional construction project management",
            "description_az": "Peşəkar tikinti layihəsi idarəetməsi",
            "description_ru": "Профессиональное управление строительными проектами",
            "slug": "construction-management",
            "order": 2
        },
        {
            "name": "Investment Advisory",
            "name_en": "Investment Advisory",
            "name_az": "İnvestisiya Məsləhəti",
            "name_ru": "Инвестиционное Консультирование",
            "description": "Expert investment advice and portfolio management",
            "description_en": "Expert investment advice and portfolio management",
            "description_az": "Ekspert investisiya məsləhəti və portfel idarəetməsi",
            "description_ru": "Экспертные инвестиционные консультации и управление портфелем",
            "slug": "investment-advisory",
            "order": 3
        }
    ]
    
    for service_data in services_data:
        # Check if service already exists
        existing = db.query(Service).filter(Service.slug == service_data["slug"]).first()
        if not existing:
            service = Service(**service_data)
            db.add(service)
            print(f"Added service: {service_data['name_en']}")
    
    db.commit()

def populate_property_sectors(db: Session):
    """Populate property sectors with multilingual data"""
    print("Populating property sectors...")
    
    sectors_data = [
        {
            "title": "Residential",
            "title_en": "Residential",
            "title_az": "Yaşayış",
            "title_ru": "Жилое",
            "description": "Residential property development and management",
            "description_en": "Residential property development and management",
            "description_az": "Yaşayış əmlakının inkişafı və idarəetməsi",
            "description_ru": "Развитие и управление жилой недвижимостью",
            "order": 1
        },
        {
            "title": "Commercial",
            "title_en": "Commercial",
            "title_az": "Kommersiya",
            "title_ru": "Коммерческое",
            "description": "Commercial real estate solutions",
            "description_en": "Commercial real estate solutions",
            "description_az": "Kommersiya daşınmaz əmlak həlləri",
            "description_ru": "Коммерческие решения в сфере недвижимости",
            "order": 2
        },
        {
            "title": "Industrial",
            "title_en": "Industrial",
            "title_az": "Sənaye",
            "title_ru": "Промышленное", 
            "description": "Industrial property development",
            "description_en": "Industrial property development",
            "description_az": "Sənaye əmlakının inkişafı",
            "description_ru": "Развитие промышленной недвижимости",
            "order": 3
        }
    ]
    
    for sector_data in sectors_data:
        # Check if sector already exists
        existing = db.query(PropertySector).filter(PropertySector.title == sector_data["title"]).first()
        if not existing:
            sector = PropertySector(**sector_data)
            db.add(sector)
            print(f"Added property sector: {sector_data['title_en']}")
    
    db.commit()

def populate_team_members(db: Session):
    """Populate team members with multilingual data"""
    print("Populating team members...")
    
    team_data = [
        {
            "full_name": "John Smith",
            "full_name_en": "John Smith",
            "full_name_az": "Con Smit",
            "full_name_ru": "Джон Смит",
            "role": "CEO & Founder",
            "role_en": "CEO & Founder",
            "role_az": "Baş İcraçı Direktor və Təsisçi",
            "role_ru": "Генеральный директор и основатель",
            "order": 1
        },
        {
            "full_name": "Sarah Johnson",
            "full_name_en": "Sarah Johnson", 
            "full_name_az": "Sara Conson",
            "full_name_ru": "Сара Джонсон",
            "role": "Project Manager",
            "role_en": "Project Manager",
            "role_az": "Layihə Meneceri",
            "role_ru": "Менеджер проектов",
            "order": 2
        },
        {
            "full_name": "Michael Brown",
            "full_name_en": "Michael Brown",
            "full_name_az": "Maykl Braun", 
            "full_name_ru": "Михаэль Браун",
            "role": "Senior Architect",
            "role_en": "Senior Architect",
            "role_az": "Baş Memar",
            "role_ru": "Старший архитектор",
            "order": 3
        }
    ]
    
    for member_data in team_data:
        # Check if member already exists
        existing = db.query(TeamMember).filter(TeamMember.full_name == member_data["full_name"]).first()
        if not existing:
            member = TeamMember(**member_data)
            db.add(member)
            print(f"Added team member: {member_data['full_name_en']}")
    
    db.commit()

def populate_projects(db: Session):
    """Populate projects with multilingual data"""
    print("Populating projects...")
    
    projects_data = [
        {
            "title": "Azure Towers",
            "title_en": "Azure Towers",
            "title_az": "Azure Qüllələri",
            "title_ru": "Лазурные Башни",
            "description": "Luxury residential complex in the city center",
            "description_en": "Luxury residential complex in the city center",
            "description_az": "Şəhər mərkəzində lüks yaşayış kompleksi",
            "description_ru": "Роскошный жилой комплекс в центре города",
            "tag": "residential",
            "client": "Azure Development",
            "year": 2023,
            "property_sector_id": 1
        },
        {
            "title": "Business Plaza",
            "title_en": "Business Plaza",
            "title_az": "Biznes Plaza",
            "title_ru": "Бизнес Плаза",
            "description": "Modern office complex with retail spaces",
            "description_en": "Modern office complex with retail spaces",
            "description_az": "Pərakəndə satış sahələri olan müasir ofis kompleksi",
            "description_ru": "Современный офисный комплекс с торговыми площадями",
            "tag": "commercial",
            "client": "Commercial Ventures",
            "year": 2024,
            "property_sector_id": 2
        }
    ]
    
    for project_data in projects_data:
        # Check if project already exists
        existing = db.query(Project).filter(Project.title == project_data["title"]).first()
        if not existing:
            project = Project(**project_data)
            db.add(project)
            print(f"Added project: {project_data['title_en']}")
    
    db.commit()

def main():
    """Main function to populate all sample data"""
    print("Starting database population with multilingual sample data...")
    
    db = SessionLocal()
    try:
        populate_services(db)
        populate_property_sectors(db)
        populate_team_members(db)
        populate_projects(db)
        print("Database population completed successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()