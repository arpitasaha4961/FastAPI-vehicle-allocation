**FastAPI Vehicle Allocation**

 


### Prerequisites 

To run this FastAPI application, you will need the following software installed:

- **Python**
- **pip**: Comes with Python installations (for managing dependencies)
- **Docker**: Version 20.10 or higher (for containerization)
- **Docker Compose**: Version 1.27 or higher (for running multi-container applications)
- **MongoDB**: A running instance (either locally or via Docker)

### Optional

- **Virtual Environment**: It's recommended to use a virtual environment to manage dependencies, such as `venv` or `virtualenv`.



### Setup

1. . Clone the repository:
   ```bash
   git clone <repo-url>
   cd vehicle-allocation
   ```
3. Run ```python -m venv venv``` 
4. Activate the virtual environment
4. If run locally then use following steps:
   ```bash
   pip install -r requirements.txt
   fastapi run .\app\main.py
   ```
   
  OR Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

6. Access the app at http://localhost:8000/docs



### Folder-Structure

```
│
├── app/
│   ├── main.py             # FastAPI Entry Point
│   ├── models.py           # MongoDB Models
│   ├── crud.py             # CRUD Logic
│   ├── __init__.py      
│   ├── db.py               # MongoDB Connection Logic
├── test/                   # Unit and Integration Tests
│       └── test.py
├── Dockerfile              # Docker Configuration
├── docker-compose.yml      # MongoDB with FastAPI
├── requirements.txt        # Dependencies
└── README.md               # Setup Instructions 
```

## API Endpoints

### Root Endpoint
- **GET /**: Redirects to `/docs` where you may test the documentation.

### Employee Endpoints
- **POST /employees/**: Adds a new employee.
- **DELETE /employees/{employee_id}**: Deletes an employee by ID.

### Vehicle Endpoints
- **POST /vehicles/**: Adds a new vehicle.
- **DELETE /vehicles/{vehicle_id}**: Deletes a vehicle by ID.

### Allocation Endpoints
- **POST /allocations/**: Creates a new vehicle allocation for an employee.
- **PUT /allocations/{allocation_id}**: Updates a vehicle allocation by object ID.
- **DELETE /allocations/{allocation_id}**: Deletes a vehicle allocation objetct by ID.
- **GET /allocations/**: Retrieves all vehicle allocations and show.
- **GET /allocations/report**: Retrieves a history report of allocations, optionally filtered by vehicle ID or employee ID.


### Running Tests
To ensure that everything is functioning as expected, run the tests using pytest. Follow these steps:

1. Make sure your virtual environment is activated.
2. Run the tests by executing the following command:

   ```bash
   pytest test/test.py
   ```

### Deployment
1. Use Docker for consistent environments.
2. Host on AWS EC2 or Azure App Services.
3. Use MongoDB Atlas for cloud-hosted MongoDB.
4. Set up CI/CD pipelines with GitHub Actions for automated deployment.
