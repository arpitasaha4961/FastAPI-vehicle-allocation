from pydantic import BaseModel

# Allocation schema for creating allocations
class AllocationCreate(BaseModel):
    employee_id: int
    vehicle_id: int
    allocation_date: str  
    
# Allocation schema for updating allocations (same structure)
class AllocationUpdate(BaseModel):
    employee_id: int
    vehicle_id: int
    allocation_date: str  
