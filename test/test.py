import pytest
from httpx import AsyncClient, ASGITransport  
from fastapi import status
from app.main import app, employees  


@pytest.fixture(autouse=True)
def clear_database():
    """Fixture to clear the employees collection before each test."""
    employees.delete_many({})

@pytest.mark.asyncio
async def test_create_employee():
    """Test the creation of an employee with auto-generated ID."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        employee_data = {
            "name": "Alic",
            "department": "Engineering"
        }

        response = await client.post("/employees/", json=employee_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check if the response has the correct data
        assert data["name"] == "Alic"
        assert data["department"] == "Engineering"
        assert "id" in data 
        assert isinstance(data["id"], int)  

@pytest.mark.asyncio
async def test_create_vehicle():
    """Test creating a vehicle."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        vehicle_data = {
            "model": "Toyota",
            "driverId": 1,
            "driverName": "John Doe"
        }

        # Send POST request to create a vehicle
        response = await client.post("/vehicles/", json=vehicle_data)
        
        # Check if the vehicle was created successfully
        assert response.status_code == 200
        created_vehicle = response.json()
        assert created_vehicle["model"] == vehicle_data["model"]
        assert created_vehicle["driverId"] == vehicle_data["driverId"]
        assert created_vehicle["driverName"] == vehicle_data["driverName"]
        assert "id" in created_vehicle  