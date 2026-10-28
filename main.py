from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Infosys Employee Management API",
    version="1.0.0"
)


# Employee request model
class Employee(BaseModel):
    name: str = Field(min_length=2)
    email: str
    department: str
    salary: float = Field(gt=0)


# Temporary in-memory database
employees = {}
next_id = 1


# Home API
@app.get("/")
def home():
    return {"message": "Employee Management API is running"}


# Add employee
@app.post("/employees", status_code=201)
def add_employee(employee: Employee):
    global next_id
    
    employee_data = employee.model_dump()
    employee_data["id"] = next_id
    employees[next_id] = employee_data
    next_id += 1
    
    return {
        "message": "Employee added successfully",
        "employee": employee_data
    }


# Get all employees
@app.get("/employees")
def get_employees():
    return list(employees.values())


# Get employee by ID
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    if employee_id not in employees:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    return employees[employee_id]


# Update employee
@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    if employee_id not in employees:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    employee_data = employee.model_dump()
    employee_data["id"] = employee_id
    employees[employee_id] = employee_data
    return {
        "message": "Employee updated successfully",
        "employee": employee_data
    }


# Delete employee
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    if employee_id not in employees:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    del employees[employee_id]
    return {"message": "Employee deleted successfully"}
