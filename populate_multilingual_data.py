"""
Script to populate database with sample multilingual data
"""
import asyncio
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.services import Service
from app.models.projects import Project
from app.models.team import TeamMember
from app.models.property_sectors import PropertySector
from app.models.about import About
from app.models.approaches import Approach
from app.models.partners import Partner
from app.models.work_process import WorkProcess

# Sample multilingual data
SAMPLE_SERVICES = [
    {
        "name": "Real Estate Development",
        "name_en": "Real Estate Development",
        "name_az": "Daşınmaz Əmlak İnkişafı",
        "name_ru": "Развитие Недвижимости",
        "description": "Comprehensive real estate development services",
        "description_en": "Comprehensive real estate development services including planning, construction, and project management",
        "description_az": "Planlaşdırma, tikinti və layihə idarəetməsi daxil olmaqla hərtərəfli daşınmaz əmlak inkişaf xidmətləri",
        "description_ru": "Комплексные услуги по развитию недвижимости, включая планирование, строительство и управление проектами",
        "slug": "real-estate-development",
        "order": 1
    },
    {
        "name": "Construction Management",
        "name_en": "Construction Management",
        "name_az": "Tikinti İdarəetməsi",
        "name_ru": "Управление Строительством",
        "description": "Professional construction management services",
        "description_en": "Professional construction management services for all types of projects",
        "description_az": "Bütün növ layihələr üçün peşəkar tikinti idarəetmə xidmətləri",
        "description_ru": "Профессиональные услуги по управлению строительством для всех типов проектов",
        "slug": "construction-management",
        "order": 2
    }
]

SAMPLE_PROJECTS = [
    {
        "title": "Modern Office Complex",
        "title_en": "Modern Office Complex",
        "title_az": "Müasir Ofis Kompleksi",
        "title_ru": "Современный Офисный Комплекс",
        "description": "A state-of-the-art office building in the city center",
        "description_en": "A state-of-the-art office building in the city center with modern amenities",
        "description_az": "Şəhər mərkəzində müasir imkanları olan ən müasir ofis binası",
        "description_ru": "Современное офисное здание в центре города с современными удобствами",
        "client": "Business Corp",
        "year": 2023,
        "tag": "commercial"
    },
    {
        "title": "Luxury Residential Tower",
        "title_en": "Luxury Residential Tower",
        "title_az": "Lüks Yaşayış Qülləsi",
        "title_ru": "Роскошная Жилая Башня",
        "description": "High-end residential tower with premium facilities",
        "description_en": "High-end residential tower with premium facilities and services",
        "description_az": "Premium imkanlar və xidmətlərlə yüksək səviyyəli yaşayış qülləsi",
        "description_ru": "Элитная жилая башня с премиальными удобствами и услугами",
        "client": "Residential Group",
        "year": 2024,
        "tag": "residential"
    }
]

SAMPLE_TEAM_MEMBERS = [
    {
        "full_name": "John Smith",
        "full_name_en": "John Smith",
        "full_name_az": "Con Smit",
        "full_name_ru": "Джон Смит",
        "role": "CEO & Founder",
        "role_en": "CEO & Founder",
        "role_az": "Baş İcraçı Direktor və Təsisçi",
        "role_ru": "Генеральный директор и основатель"
    },
    {
        "full_name": "Maria Garcia",
        "full_name_en": "Maria Garcia",
        "full_name_az": "Mariya Qarsiya",
        "full_name_ru": "Мария Гарсия",
        "role": "Head of Projects",
        "role_en": "Head of Projects",
        "role_az": "Layihələr Rəhbəri",
        "role_ru": "Руководитель проектов"
    }
]

SAMPLE_PROPERTY_SECTORS = [
    {
        "title": "Commercial Real Estate",
        "title_en": "Commercial Real Estate",
        "title_az": "Kommersiya Daşınmaz Əmlakı",
        "title_ru": "Коммерческая Недвижимость",
        "description": "Office buildings, retail spaces, and commercial complexes",
        "description_en": "Office buildings, retail spaces, and commercial complexes",
        "description_az": "Ofis binaları, pərakəndə satış sahələri və kommersiya kompleksləri",
        "description_ru": "Офисные здания, торговые помещения и коммерческие комплексы",
        "order": 1
    },
    {
        "title": "Residential Projects",
        "title_en": "Residential Projects",
        "title_az": "Yaşayış Layihələri",
        "title_ru": "Жилые Проекты",
        "description": "Apartments, villas, and residential communities",
        "description_en": "Apartments, villas, and residential communities",
        "description_az": "Mənzillər, villalar və yaşayış icmaları",
        "description_ru": "Квартиры, виллы и жилые комплексы",
        "order": 2
    }
]

SAMPLE_ABOUT = [
    {
        "experience": "15+ Years",
        "experience_en": "15+ Years",
        "experience_az": "15+ İl",
        "experience_ru": "15+ Лет",
        "project_count": "200+ Projects",
        "project_count_en": "200+ Projects",
        "project_count_az": "200+ Layihə",
        "project_count_ru": "200+ Проектов",
        "members": "50+ Team Members",
        "members_en": "50+ Team Members",
        "members_az": "50+ Komanda Üzvü",
        "members_ru": "50+ Членов Команды"
    }
]

SAMPLE_APPROACHES = [
    {
        "title": "Innovation First",
        "title_en": "Innovation First",
        "title_az": "İlk Növbədə İnnovasiya",
        "title_ru": "Инновации Прежде Всего",
        "description": "We prioritize innovative solutions in all our projects",
        "description_en": "We prioritize innovative solutions in all our projects",
        "description_az": "Bütün layihələrimizdə innovativ həllərə üstünlük veririk",
        "description_ru": "Мы приоритизируем инновационные решения во всех наших проектах",
        "order": 1
    },
    {
        "title": "Quality Assurance",
        "title_en": "Quality Assurance",
        "title_az": "Keyfiyyət Təminatı",
        "title_ru": "Обеспечение Качества",
        "description": "Every project meets the highest quality standards",
        "description_en": "Every project meets the highest quality standards",
        "description_az": "Hər layihə ən yüksək keyfiyyət standartlarına cavab verir",
        "description_ru": "Каждый проект соответствует самым высоким стандартам качества",
        "order": 2
    }
]

SAMPLE_PARTNERS = [
    {
        "title": "Our Partners",
        "title_en": "Our Partners",
        "title_az": "Tərəfdaşlarımız",
        "title_ru": "Наши Партнеры",
        "button_text": "Learn More",
        "button_text_en": "Learn More",
        "button_text_az": "Daha Çox Öyrən",
        "button_text_ru": "Узнать Больше"
    }
]

SAMPLE_WORK_PROCESSES = [
    {
        "title": "Planning & Design",
        "title_en": "Planning & Design",
        "title_az": "Planlaşdırma və Dizayn",
        "title_ru": "Планирование и Дизайн",
        "description": "Comprehensive planning and architectural design phase",
        "description_en": "Comprehensive planning and architectural design phase",
        "description_az": "Hərtərəfli planlaşdırma və memarlıq dizayn mərhələsi",
        "description_ru": "Комплексная фаза планирования и архитектурного проектирования",
        "order": 1
    },
    {
        "title": "Construction",
        "title_en": "Construction",
        "title_az": "Tikinti",
        "title_ru": "Строительство",
        "description": "Professional construction with quality monitoring",
        "description_en": "Professional construction with quality monitoring",
        "description_az": "Keyfiyyət monitorinqi ilə peşəkar tikinti",
        "description_ru": "Профессиональное строительство с контролем качества",
        "order": 2
    }
]

def populate_services(db: Session):
    """Populate services with multilingual data"""
    print("Populating services...")
    for service_data in SAMPLE_SERVICES:
        # Check if service already exists
        existing = db.query(Service).filter(Service.slug == service_data["slug"]).first()
        if not existing:
            service = Service(**service_data)
            db.add(service)
    db.commit()
    print("Services populated!")

def populate_projects(db: Session):
    """Populate projects with multilingual data"""
    print("Populating projects...")
    for project_data in SAMPLE_PROJECTS:
        # Check if project already exists
        existing = db.query(Project).filter(Project.title == project_data["title"]).first()
        if not existing:
            project = Project(**project_data)
            db.add(project)
    db.commit()
    print("Projects populated!")

def populate_team_members(db: Session):
    """Populate team members with multilingual data"""
    print("Populating team members...")
    for member_data in SAMPLE_TEAM_MEMBERS:
        # Check if team member already exists
        existing = db.query(TeamMember).filter(TeamMember.full_name == member_data["full_name"]).first()
        if not existing:
            member = TeamMember(**member_data)
            db.add(member)
    db.commit()
    print("Team members populated!")

def populate_property_sectors(db: Session):
    """Populate property sectors with multilingual data"""
    print("Populating property sectors...")
    for sector_data in SAMPLE_PROPERTY_SECTORS:
        # Check if property sector already exists
        existing = db.query(PropertySector).filter(PropertySector.title == sector_data["title"]).first()
        if not existing:
            sector = PropertySector(**sector_data)
            db.add(sector)
    db.commit()
    print("Property sectors populated!")

def populate_about(db: Session):
    """Populate about sections with multilingual data"""
    print("Populating about sections...")
    for about_data in SAMPLE_ABOUT:
        # Check if about section already exists
        existing = db.query(About).first()
        if not existing:
            about = About(**about_data)
            db.add(about)
    db.commit()
    print("About sections populated!")

def populate_approaches(db: Session):
    """Populate approaches with multilingual data"""
    print("Populating approaches...")
    for approach_data in SAMPLE_APPROACHES:
        # Check if approach already exists
        existing = db.query(Approach).filter(Approach.title == approach_data["title"]).first()
        if not existing:
            approach = Approach(**approach_data)
            db.add(approach)
    db.commit()
    print("Approaches populated!")

def populate_partners(db: Session):
    """Populate partners with multilingual data"""
    print("Populating partners...")
    for partner_data in SAMPLE_PARTNERS:
        # Check if partner already exists
        existing = db.query(Partner).filter(Partner.title == partner_data["title"]).first()
        if not existing:
            partner = Partner(**partner_data)
            db.add(partner)
    db.commit()
    print("Partners populated!")

def populate_work_processes(db: Session):
    """Populate work processes with multilingual data"""
    print("Populating work processes...")
    for wp_data in SAMPLE_WORK_PROCESSES:
        # Check if work process already exists
        existing = db.query(WorkProcess).filter(WorkProcess.title == wp_data["title"]).first()
        if not existing:
            wp = WorkProcess(**wp_data)
            db.add(wp)
    db.commit()
    print("Work processes populated!")

def main():
    """Main function to populate all multilingual data"""
    print("Starting to populate multilingual data...")
    
    # Get database session
    db = next(get_db())
    
    try:
        populate_services(db)
        populate_projects(db)
        populate_team_members(db)
        populate_property_sectors(db)
        populate_about(db)
        populate_approaches(db)
        populate_partners(db)
        populate_work_processes(db)
        
        print("\n✅ All multilingual data populated successfully!")
        print("\nYou can now test the multilingual endpoints:")
        print("- http://localhost:8000/services?language=en")
        print("- http://localhost:8000/services?language=az")
        print("- http://localhost:8000/services?language=ru")
        print("- http://localhost:8000/projects?language=en")
        print("- http://localhost:8000/team-members?language=az")
        print("- And so on...")
        
    except Exception as e:
        print(f"❌ Error populating data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()