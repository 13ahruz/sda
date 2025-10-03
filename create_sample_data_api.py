import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def create_services():
    """Create sample services via API"""
    print("Creating sample services...")
    
    services = [
        {
            "name": "Real Estate Development",
            "description": "Comprehensive real estate development services",
            "order": 1
        },
        {
            "name": "Construction Management", 
            "description": "Professional construction project management",
            "order": 2
        },
        {
            "name": "Investment Advisory",
            "description": "Expert investment advice and portfolio management",
            "order": 3
        }
    ]
    
    for service in services:
        try:
            response = requests.post(f"{BASE_URL}/services/json", json=service)
            if response.status_code == 200:
                print(f"✓ Created service: {service['name']}")
            else:
                print(f"✗ Failed to create service: {service['name']} - {response.text}")
        except Exception as e:
            print(f"✗ Error creating service: {service['name']} - {e}")

def create_property_sectors():
    """Create sample property sectors via API"""
    print("Creating sample property sectors...")
    
    sectors = [
        {
            "title": "Residential",
            "description": "Residential property development and management",
            "order": 1
        },
        {
            "title": "Commercial", 
            "description": "Commercial real estate solutions",
            "order": 2
        },
        {
            "title": "Industrial",
            "description": "Industrial property development",
            "order": 3
        }
    ]
    
    for sector in sectors:
        try:
            # Use form data as per the API
            response = requests.post(f"{BASE_URL}/property-sectors", data=sector)
            if response.status_code == 200:
                print(f"✓ Created property sector: {sector['title']}")
            else:
                print(f"✗ Failed to create property sector: {sector['title']} - {response.text}")
        except Exception as e:
            print(f"✗ Error creating property sector: {sector['title']} - {e}")

def create_team_members():
    """Create sample team members via API"""
    print("Creating sample team members...")
    
    members = [
        {
            "full_name": "John Smith",
            "role": "CEO & Founder"
        },
        {
            "full_name": "Sarah Johnson",
            "role": "Project Manager"
        },
        {
            "full_name": "Michael Brown",
            "role": "Senior Architect"
        }
    ]
    
    for member in members:
        try:
            # Use form data as per the API
            response = requests.post(f"{BASE_URL}/team-members", data=member)
            if response.status_code == 200:
                print(f"✓ Created team member: {member['full_name']}")
            else:
                print(f"✗ Failed to create team member: {member['full_name']} - {response.text}")
        except Exception as e:
            print(f"✗ Error creating team member: {member['full_name']} - {e}")

def create_approaches():
    """Create sample approaches via API"""
    print("Creating sample approaches...")
    
    approaches = [
        {
            "title": "Client-Focused Approach",
            "description": "We prioritize our clients' needs and vision in every project",
            "order": 1
        },
        {
            "title": "Sustainable Development",
            "description": "Environmental responsibility is at the core of our development philosophy",
            "order": 2
        },
        {
            "title": "Innovation & Technology",
            "description": "Leveraging cutting-edge technology for superior results",
            "order": 3
        }
    ]
    
    for approach in approaches:
        try:
            response = requests.post(f"{BASE_URL}/approaches", data=approach)
            if response.status_code == 200:
                print(f"✓ Created approach: {approach['title']}")
            else:
                print(f"✗ Failed to create approach: {approach['title']} - {response.text}")
        except Exception as e:
            print(f"✗ Error creating approach: {approach['title']} - {e}")

def main():
    """Create all sample data"""
    print("Creating sample multilingual data via API calls...")
    print("=" * 50)
    
    create_services()
    print()
    create_property_sectors()
    print()
    create_team_members()
    print()
    create_approaches()
    print()
    
    print("=" * 50)
    print("Sample data creation completed!")
    print("You can now test the multilingual endpoints with:")
    print("curl 'http://localhost:8000/api/v1/services?language=en'")
    print("curl 'http://localhost:8000/api/v1/services?language=az'")
    print("curl 'http://localhost:8000/api/v1/services?language=ru'")

if __name__ == "__main__":
    main()