from fastapi import FastAPI,HTTPException,Query
from fastapi.responses import RedirectResponse
from app.crud import create_employee, delete_employee,create_vehicle, delete_vehicle,create_allocation,delete_allocation,update_allocation,get_allocations,fetch_allocation_report
from app.models import Employee,Vehicle,Allocation,EmployeeResponse,VehicleResponse
from app.db import employees, vehicles, allocations 
from datetime import datetime
from typing import Dict
from typing import List,Optional
from bson import ObjectId


app = FastAPI(title="Vehicle Allocation API", version="1.0.0")


@app.get("/")
async def root():
    return RedirectResponse(url="http://localhost:8000/docs")

@app.post("/employees/", response_model=EmployeeResponse)
async def add_employee(employee: Employee):
    """API to add a new employee."""
    return await create_employee(employee.name, employee.department)

@app.delete("/employees/{employee_id}", response_model=dict)
async def remove_employee(employee_id: int):
    """API to delete an employee."""
    return await delete_employee(employee_id)

@app.post("/vehicles/", response_model=VehicleResponse)
async def add_vehicle(vehicle: Vehicle):
    """API to add a new vehicle."""
    return await create_vehicle(vehicle.model, vehicle.driverId, vehicle.driverName)

@app.delete("/vehicles/{vehicle_id}" , response_model=dict)
async def remove_vehicle(vehicle_id: int):
    """API to delete a vehicle."""
    return await delete_vehicle(vehicle_id)


@app.post("/allocations/", response_model=Allocation)
async def create_allocation_endpoint(allocation: Allocation):
    """Create a new vehicle allocation for an employee."""
    try:
        result = await create_allocation(
            employee_id=allocation.employee_id,
            vehicle_id=allocation.vehicle_id,
            allocation_date=allocation.allocation_date
        )
        return result
    except HTTPException as e:
        raise e  # HTTP exceptions for debug
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/allocations/{allocation_id}")
async def update_allocation_endpoint(allocation_id: str, update_data: Allocation):
    """Update a new vehicle allocation for an employee."""
    update_dict = update_data.dict()  # Converts the model instance to a dictionary
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

    result = await delete_allocation(allocation_obj_id)
    
    return result

@app.get("/allocations/", response_model=List[Allocation])
async def get_allocations():
    """Retrieve all allocations."""
    
    all_allocations = allocations.find().to_list(1000)
    return all_allocations


@app.get("/allocations/report")
async def get_allocation_report(
    vehicle_id: Optional[int] = Query(None, description="Filter by vehicle ID"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
):
    result = await fetch_allocation_report(allocations, vehicle_id, employee_id)

    if not result:
        raise HTTPException(status_code=404, detail="No allocations found with the specified filters")

    return result