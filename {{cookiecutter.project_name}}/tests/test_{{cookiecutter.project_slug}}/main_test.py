from __future__ import annotations
from fastapi.testclient import TestClient
from {{cookiecutter.project_slug}}.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the {{cookiecutter.project_name}} project!"}
