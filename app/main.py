from fastapi import FastAPI,HTTPException
from app.crud import create_employee, delete_employee,create_vehicle, delete_vehicle,create_allocation,delete_allocation,update_allocation,get_allocations
from app.models import Employee,Vehicle,Allocation
from app.db import employees, vehicles, allocations 
from datetime import datetime
from typing import Dict
from typing import List
from bson import ObjectId

app = FastAPI(title="Employee Management API", version="1.0.0")

# New root route
@app.get("/")
async def root():
    return {"message": "Welcome to the Employee Management API"}

@app.post("/employees/", response_model=Employee)
async def add_employee(employee: Employee):
    """API to add a new employee."""
    return await create_employee(employee.id, employee.name, employee.department)

@app.delete("/employees/{employee_id}", response_model=dict)
async def remove_employee(employee_id: int):
    """API to delete an employee."""
    return await delete_employee(employee_id)

@app.post("/vehicles/", response_model=Vehicle)
async def add_vehicle(vehicle: Vehicle):
    """API to add a new vehicle."""
    return await create_vehicle(vehicle.id, vehicle.model, vehicle.driverId, vehicle.driverName)

@app.delete("/vehicles/{vehicle_id}" , response_model=dict)
async def remove_vehicle(vehicle_id: int):
    """API to delete a vehicle."""
    return await delete_vehicle(vehicle_id)


@app.post("/allocations/", response_model=Allocation)
async def create_allocation(allocation: Allocation):
    """Create a new vehicle allocation for an employee."""
    
    # Check if the employee exists
    employee = employees.find_one({"id": allocation.employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    
    # Check if the vehicle exists
    vehicle = vehicles.find_one({"id": allocation.vehicle_id})
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found.")
    
    # Check if the vehicle is already allocated for the specified date
    existing_allocation = allocations.find_one({
        "vehicle_id": allocation.vehicle_id,
        "allocation_date": allocation.allocation_date
    })
    if existing_allocation:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for this date.")

    # Insert the new allocation
    allocation_dict = allocation.dict()
    allocations.insert_one(allocation_dict)
    
    return allocation_dict

@app.put("/allocations/{allocation_id}")
async def update_allocation_endpoint(allocation_id: str, update_data: Allocation):
    # Create a dictionary from the Pydantic model
    update_dict = update_data.dict()  # Converts the model instance to a dictionary

    # Call your actual update function here
    result = await update_allocation(allocation_id, update_dict)

    return result


@app.delete("/allocations/{allocation_id}")
async def delete_allocation_endpoint(allocation_id: str):
    """Delete a vehicle allocation."""
    
    # Convert the allocation_id to an ObjectId
    try:
        allocation_obj_id = ObjectId(allocation_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid allocation ID format.")

    # Call the delete function from crud.py
    result = await delete_allocation(allocation_obj_id)
    
    return result

@app.get("/allocations/", response_model=List[Allocation])
async def get_allocations():
    """Retrieve all allocations."""
    
    all_allocations = allocations.find().to_list(1000)
    return all_allocations