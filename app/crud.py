from app.db import employees,vehicles,allocations
from fastapi import HTTPException, status
from typing import List
from datetime import datetime,date
from bson import ObjectId

async def create_employee(employee_id: int, name: str, department: str):
    """Add a new employee to the system."""
    # Check if the employee already exists
    existing = employees.find_one({"id": employee_id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee already exists."
        )

    new_employee = {"id": employee_id, "name": name, "department": department}
    employees.insert_one(new_employee)
    return new_employee

async def delete_employee(employee_id: int):
    """Delete an employee from the system."""
    result = employees.delete_one({"id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found."
        )
    return {"message": "Employee deleted successfully."}

async def create_vehicle(vehicle_id: int, model: str, driverId: int, driverName: str):
    """Add a new vehicle to the system."""
    # Check if the vehicle already exists
    existing = vehicles.find_one({"id": vehicle_id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle already exists."
        )

    new_vehicle = {"id": vehicle_id, "model": model, "driverId": driverId,"driverName": driverName }
    vehicles.insert_one(new_vehicle)
    return new_vehicle

async def delete_vehicle(vehicle_id: int):
    """Delete a vehicle from the system."""
    result = vehicles.delete_one({"id": vehicle_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found."
        )
    return {"message": "Vehicle deleted successfully."}


async def create_allocation(employee_id: int, vehicle_id: int, allocation_date: datetime):
    """Create a new vehicle allocation for an employee."""

    # Check if the employee exists
    employee = employees.find_one({"id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")

    # Check if the vehicle exists
    vehicle = vehicles.find_one({"id": vehicle_id})
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found.")

    # Convert the allocation_date to just the date part for comparison
    allocation_date_only = allocation_date.date()

    # Check if the vehicle is already allocated for the specified date
    existing_allocation = allocations.find_one({
        "vehicle_id": vehicle_id,
        "allocation_date": {"$eq": allocation_date_only}  # Check for exact match on date
    })
    
    if existing_allocation:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for this date.")

    # Insert the new allocation
    allocation_dict = {
        "employee_id": employee_id,
        "vehicle_id": vehicle_id,
        "allocation_date": allocation_date_only  # Store just the date part
    }
    allocations.insert_one(allocation_dict)

    # Return a success message along with the allocation details
    return {
        "message": "Vehicle allocation created successfully.",
        "allocation": allocation_dict
    }

async def get_allocation(allocation_id: str):
    """Retrieve an allocation by its ObjectId."""
    
    # Convert the allocation_id from string to ObjectId
    try:
        allocation_id_obj = ObjectId(allocation_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid allocation ID format.")
    
    # Fetch the allocation from the database
    allocation = allocations.find_one({"_id": allocation_id_obj})
    
    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found.")
    
    return allocation
    

def validate_object_id(id: str):
    if ObjectId.is_valid(id):
        return ObjectId(id)
    else:
        raise HTTPException(status_code=400, detail="Invalid ObjectId")

# Function to update allocation in the MongoDB collection
async def update_allocation(allocation_id: ObjectId, update_data: dict):
    allocation_obj_id = validate_object_id(allocation_id)

    result = allocations.update_one(
        {"_id": allocation_obj_id},
        {"$set": update_data}
    )

    if result.modified_count == 1:
        # If the allocation was updated, return a success message along with updated data
        updated_allocation = allocations.find_one({"_id": allocation_obj_id})  # Fetch updated data if needed

        if updated_allocation:
            updated_allocation["_id"] = str(updated_allocation["_id"])

        return {
            "message": "Allocation updated successfully.",
            "updated_data": updated_allocation
        }
    else:
        raise HTTPException(status_code=404, detail="Allocation not found.")

async def delete_allocation(allocation_id: ObjectId):
    """Delete a vehicle allocation."""
    
    result = allocations.delete_one({"_id": allocation_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Allocation not found.")
    
    return {"message": "Allocation deleted successfully."}


async def get_allocations() -> List[dict]:
    """Retrieve all allocations."""
    
    all_allocations = allocations.find().to_list(1000)
    return all_allocations