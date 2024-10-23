# test_employee.py
import pytest
from httpx import AsyncClient
from fastapi import status
from main import app, employees  # Import FastAPI app and employees collection

@pytest.fixture(autouse=True)
def clear_database():
    """Fixture to clear the employees collection before each test."""
    employees.delete_many({})

@pytest.mark.asyncio
async def test_create_employee():
    """Test the creation of an employee with auto-generated ID."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        employee_data = {
            "name": "Alice",
            "department": "Engineering"
        }

        response = await client.post("/employees/", json=employee_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check if the response has the correct data
        assert data["name"] == "Alice"
        assert data["department"] == "Engineering"
        assert "id" in data  # Ensure `id` is auto-generated and returned as part of the response
        assert isinstance(data["id"], int)  # Confirm `id` is an integer

@pytest.mark.asyncio
async def test_create_employee_duplicate_name():
    """Test failure when creating an employee with a duplicate name."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        employee_data = {
            "name": "Bob",
            "department": "Finance"
        }

        # First creation should succeed
        response = await client.post("/employees/", json=employee_data)
        assert response.status_code == status.HTTP_200_OK

        # Second creation with the same name should fail
        response = await client.post("/employees/", json=employee_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Employee already exists."
