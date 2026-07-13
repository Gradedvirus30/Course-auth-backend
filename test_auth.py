import requests

BASE_URL = "http://127.0.0.1:8000"

# Login as admin
login_response = requests.post(
    f"{BASE_URL}/auth/admin/login",
    data={
        "username": "admin",
        "password": "admin123",
    },
)

print("Login Status:", login_response.status_code)
print(login_response.json())

token = login_response.json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}"
}

# Create a course
course_response = requests.post(
    f"{BASE_URL}/admin/courses",
    json={
        "course_name": "AI",
        "description": "Beginner AI Course"
    },
    headers=headers,
)

print("Create Course Status:", course_response.status_code)
print(course_response.json())