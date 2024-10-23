from pydantic import BaseModel
from datetime import datetime

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


    