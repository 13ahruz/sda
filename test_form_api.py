"""
Test script to demonstrate how to use the new form-based API endpoints
with file uploads instead of JSON with string URLs.
"""

import requests
import json
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_create_project_with_file():
    """Test creating a project with form data and file upload"""
    print("Testing project creation with form data...")
    
    # Prepare form data
    data = {
        'title': 'Modern Office Building',
        'tag': 'Commercial',
        'client': 'ABC Corp',
        'year': 2024,
        'property_sector_id': 1
    }
    
    # If you have an image file, uncomment this:
    # files = {'cover_photo': open('sample_image.jpg', 'rb')}
    files = {}  # No file for this test
    
    response = requests.post(f"{BASE_URL}/projects", data=data, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_create_service_with_file():
    """Test creating a service with form data and file upload"""
    print("\nTesting service creation with form data...")
    
    data = {
        'title': 'Property Management',
        'description': 'Complete property management services',
        'order': 1
    }
    
    files = {}  # No icon for this test
    
    response = requests.post(f"{BASE_URL}/services", data=data, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_create_news_with_file():
    """Test creating news with form data and file upload"""
    print("\nTesting news creation with form data...")
    
    data = {
        'title': 'Market Update Q4 2024',
        'content': 'The real estate market shows positive trends...',
        'tags': 'market,update,2024'  # Comma-separated
    }
    
    files = {}  # No photo for this test
    
    response = requests.post(f"{BASE_URL}/news", data=data, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_create_team_member_with_file():
    """Test creating a team member with form data and file upload"""
    print("\nTesting team member creation with form data...")
    
    data = {
        'name': 'John Doe',
        'position': 'Senior Agent',
        'department': 'Sales',
        'bio': 'Experienced real estate professional...',
        'display_order': 1
    }
    
    files = {}  # No photo for this test
    
    response = requests.post(f"{BASE_URL}/team-members", data=data, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_upload_project_photo():
    """Test uploading additional photos to a project"""
    print("\nTesting project photo upload...")
    
    # First create a project
    project = test_create_project_with_file()
    if not project:
        print("Failed to create project for photo test")
        return
    
    project_id = project['id']
    
    # If you have an image file, uncomment this:
    # files = {'file': open('sample_photo.jpg', 'rb')}
    # params = {'order': 1}
    # response = requests.post(f"{BASE_URL}/projects/{project_id}/photos", files=files, params=params)
    # print(f"Photo upload status: {response.status_code}")
    # print(f"Photo upload response: {response.json()}")

if __name__ == "__main__":
    print("Testing Form-based API with File Uploads")
    print("=" * 50)
    
    try:
        test_create_project_with_file()
        test_create_service_with_file()
        test_create_news_with_file()
        test_create_team_member_with_file()
        test_upload_project_photo()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed!")
        print("\nTo test with actual files:")
        print("1. Put sample images in the same directory as this script")
        print("2. Uncomment the file upload lines in the test functions")
        print("3. Run the script again")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure the API is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
