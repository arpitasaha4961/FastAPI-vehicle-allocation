from pydantic import BaseModel,Field
from datetime import datetime
from bson import ObjectId

class Employee(BaseModel):
    name: str
    department: str

class EmployeeResponse(Employee):
    id: int 


class Vehicle(BaseModel):
    model: str
    driverId: int
    driverName: str

class VehicleResponse(Vehicle):
    id: int 

class Allocation(BaseModel):
    
    employee_id: int
    vehicle_id: int
    allocation_date: datetime

class AllocationResponse(Allocation):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")

    