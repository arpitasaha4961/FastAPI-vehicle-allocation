from pydantic import BaseModel
from datetime import datetime

class Employee(BaseModel):
    id: int
    name: str
    department: str

class Vehicle(BaseModel):
    id: int
    model: str
    driverId: int
    driverName: str

class Allocation(BaseModel):
    employee_id: int
    vehicle_id: int
    allocation_date: datetime