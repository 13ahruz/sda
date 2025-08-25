import requests

# Test the projects endpoint
url = "http://localhost:8000/api/v1/projects"

# Test data for form submission
data = {
    "title": "Test Project",
    "tag": "residential", 
    "client": "Test Client",
    "year": 2024
}

try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
