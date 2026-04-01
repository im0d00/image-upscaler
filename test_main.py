import pytest
import requests

BASE_URL = "http://localhost:8000"  # Update with your actual backend URL


def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_validation():
    # Testing valid file upload
    files = {'file': open('valid_image.png', 'rb')}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    assert response.status_code == 200
    assert "upload_id" in response.json()

    # Testing invalid file upload
    files = {'file': open('invalid_file.txt', 'rb')}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    assert response.status_code == 400
    assert "error" in response.json()


def test_task_management():
    # Assume a valid upload returns an upload ID
    files = {'file': open('valid_image.png', 'rb')}
    upload_response = requests.post(f"{BASE_URL}/upload", files=files)
    upload_id = upload_response.json()["upload_id"]

    # Start processing task
    response = requests.post(f"{BASE_URL}/tasks/{upload_id}/start")
    assert response.status_code == 202

    # Check task status
    response = requests.get(f"{BASE_URL}/tasks/{upload_id}")
    assert response.status_code == 200
    assert response.json()["status"] in ["processing", "completed", "failed"]


def test_status_polling():
    # Assume we have a valid upload ID to poll status for
    upload_id = "valid_upload_id"
    response = requests.get(f"{BASE_URL}/tasks/{upload_id}")
    assert response.status_code == 200
    assert "status" in response.json()


def test_error_handling():
    # Test endpoint that does not exist
    response = requests.get(f"{BASE_URL}/invalid-endpoint")
    assert response.status_code == 404
    assert "error" in response.json()
    
    # Test bad request
    response = requests.post(f"{BASE_URL}/upload", files={})  # No files uploaded
    assert response.status_code == 400
    assert "error" in response.json()


if __name__ == "__main__":
    pytest.main()