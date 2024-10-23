from app.db import employees,vehicles,allocations
from fastapi import HTTPException, status,Query
from typing import List,Optional
from datetime import datetime,date,time
from bson import ObjectId
import pytz  


UTC = pytz.UTC

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

def ensure_datetime(input_date: date | datetime) -> datetime:
    """Ensure the input is a datetime object."""
    if isinstance(input_date, date) and not isinstance(input_date, datetime):
        return datetime.combine(input_date, time.min)
    return input_date 


async def create_allocation(employee_id: int, vehicle_id: int, allocation_date: datetime):
    """Create a new vehicle allocation for an employee."""
    
    # Ensure both allocation_date and current datetime are timezone-aware
    if allocation_date.tzinfo is None:  # Check if allocation_date is naive
        allocation_date = UTC.localize(allocation_date) 
    current_datetime = datetime.now(UTC) 

    # Check if the employee exists
    employee = employees.find_one({"id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")

    # Check if the vehicle exists
    vehicle = vehicles.find_one({"id": vehicle_id})
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found.")

    if allocation_date <= current_datetime:  # Use the timezone-aware current datetime
        raise HTTPException(status_code=400, detail="Allocation date must be in the future.")

    # Convert the allocation_date to datetime if it's not already
    formatted_date = ensure_datetime(allocation_date)

    # Check if the vehicle is already allocated for the specified date
    existing_allocation = allocations.find_one({
        "vehicle_id": vehicle_id,
        "allocation_date": {"$eq": formatted_date}  # Check for exact match on datetime
    })

    if existing_allocation:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for this date.")

    # Insert the new allocation
    allocation_dict = {
        "employee_id": employee_id,
        "vehicle_id": vehicle_id,
        "allocation_date": formatted_date  # Store as datetime
    }
    allocations.insert_one(allocation_dict)

    # Prepare and return the response with the correct structure
    response = {
        "employee_id": employee_id,
        "vehicle_id": vehicle_id,
        "allocation_date": formatted_date.isoformat()  
    }
    return response


async def get_allocation(allocation_id: str):
    """Retrieve an allocation by its ObjectId."""
    
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


async def update_allocation(allocation_id: str, update_data: dict):
    """Update an allocation by its ObjectId."""
    allocation_obj_id = validate_object_id(allocation_id)

    # Fetch the existing allocation to check the date
    existing_allocation = allocations.find_one({"_id": allocation_obj_id})

    if not existing_allocation:
        raise HTTPException(status_code=404, detail="Allocation not found.")

    # Check if the allocation date is in the past
    allocation_date = existing_allocation["allocation_date"]

    # Ensure the allocation_date is timezone-aware
    if allocation_date.tzinfo is None:  # Check if naive
        allocation_date = UTC.localize(allocation_date)  # Localize to UTC

    # Ensure the current datetime is timezone-aware
    current_datetime = datetime.now(UTC)

    # Compare the dates
    if allocation_date < current_datetime:
        raise HTTPException(status_code=400, detail="Cannot update allocation for past dates.")

    # Proceed with the update
    result = allocations.update_one(
        {"_id": allocation_obj_id},
        {"$set": update_data}
    )

    if result.modified_count == 1:
        updated_allocation = allocations.find_one({"_id": allocation_obj_id})  # Fetch updated data if needed
        if updated_allocation:
            updated_allocation["_id"] = str(updated_allocation["_id"])

        return {
            "message": "Allocation updated successfully.",
            "updated_data": updated_allocation
        }
    else:
        raise HTTPException(status_code=404, detail="Allocation not found.")


async def delete_allocation(allocation_id: str):
    """Delete a vehicle allocation."""
    allocation_obj_id = validate_object_id(allocation_id)
    
    # Fetch the existing allocation to check the date
    existing_allocation = allocations.find_one({"_id": allocation_obj_id})

    if not existing_allocation:
        raise HTTPException(status_code=404, detail="Allocation not found.")

    # Check if the allocation date is in the past
    allocation_date = existing_allocation["allocation_date"]

    # Ensure the allocation_date is timezone-aware
    if allocation_date.tzinfo is None:  # Check if naive
        allocation_date = UTC.localize(allocation_date)  # Localize to UTC

    # Ensure the current datetime is timezone-aware
    current_datetime = datetime.now(UTC)

    # Compare the dates
    if allocation_date < current_datetime:
        raise HTTPException(status_code=400, detail="Cannot delete allocation for past dates.")

    result = allocations.delete_one({"_id": allocation_obj_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Allocation not found.")
    
    return {"message": "Allocation deleted successfully."}




async def get_allocations() -> List[dict]:
    """Retrieve all allocations."""
    
    all_allocations = allocations.find().to_list(1000)
    return all_allocations


def serialize_allocation(allocation):
    """Convert ObjectId to string and format dates."""
    return {
        "id": str(allocation["_id"]),
        "employee_id": allocation["employee_id"],
        "vehicle_id": allocation["vehicle_id"],
        "allocation_date": allocation["allocation_date"].isoformat(),
    }

async def fetch_allocation_report(
    allocations,
    vehicle_id: Optional[str] = None,
    employee_id: Optional[int] = None,
) -> List[dict]:
    """Fetch allocation report from the database."""
    
    query = {}
    if vehicle_id:
        query["vehicle_id"] = vehicle_id
    if employee_id is not None:  # Check for None explicitly
        query["employee_id"] = employee_id


    allocations_query = allocations.find(query)
    
    # Serialize the allocations to make them JSON-compatible
    result = [serialize_allocation(allocation) for allocation in allocations_query]

    return result