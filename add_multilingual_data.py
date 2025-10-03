"""
Quick script to add multilingual data directly to database using SQL
"""
import psycopg2
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """Get database connection"""
    conn = psycopg2.connect(
        host="localhost",
        database="sda_local_db",
        user="postgres",
        password="postgres123",
        port="5432"
    )
    try:
        yield conn
    finally:
        conn.close()

def add_service_multilingual_data():
    """Add multilingual data to services"""
    print("Adding multilingual data to services...")
    
    multilingual_updates = [
        {
            "id": 1,
            "name_en": "Real Estate Development",
            "name_az": "Daşınmaz Əmlak İnkişafı", 
            "name_ru": "Развитие Недвижимости",
            "description_en": "Comprehensive real estate development services",
            "description_az": "Hərtərəfli daşınmaz əmlak inkişaf xidmətləri",
            "description_ru": "Комплексные услуги по развитию недвижимости"
        },
        {
            "id": 2,
            "name_en": "Construction Management",
            "name_az": "Tikinti İdarəetməsi",
            "name_ru": "Управление Строительством", 
            "description_en": "Professional construction project management",
            "description_az": "Peşəkar tikinti layihəsi idarəetməsi",
            "description_ru": "Профессиональное управление строительными проектами"
        }
    ]
    
    with get_db_connection() as conn:
        cur = conn.cursor()
        
        for update in multilingual_updates:
            sql = """
            UPDATE services 
            SET name_en = %s, name_az = %s, name_ru = %s,
                description_en = %s, description_az = %s, description_ru = %s
            WHERE id = %s
            """
            cur.execute(sql, (
                update["name_en"], update["name_az"], update["name_ru"],
                update["description_en"], update["description_az"], update["description_ru"],
                update["id"]
            ))
            print(f"✓ Updated service ID {update['id']}")
        
        conn.commit()
        cur.close()

def create_property_sectors():
    """Create property sectors with multilingual data"""
    print("Creating property sectors with multilingual data...")
    
    sectors = [
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
        }
    ]
    
    with get_db_connection() as conn:
        cur = conn.cursor()
        
        for sector in sectors:
            # Check if already exists
            cur.execute("SELECT id FROM property_sectors WHERE title = %s", (sector["title"],))
            if not cur.fetchone():
                sql = """
                INSERT INTO property_sectors (title, title_en, title_az, title_ru, 
                                            description, description_en, description_az, description_ru, "order")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(sql, (
                    sector["title"], sector["title_en"], sector["title_az"], sector["title_ru"],
                    sector["description"], sector["description_en"], sector["description_az"], sector["description_ru"],
                    sector["order"]
                ))
                print(f"✓ Created property sector: {sector['title']}")
        
        conn.commit()
        cur.close()

def main():
    """Run all multilingual data updates"""
    print("Adding multilingual data to database...")
    print("=" * 50)
    
    try:
        add_service_multilingual_data()
        print()
        create_property_sectors()
        print()
        print("=" * 50)
        print("Multilingual data successfully added!")
        print("Test with: curl 'http://localhost:8000/api/v1/services?language=az'")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()