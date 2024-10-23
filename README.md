# FastAPI-vehicle-allocation

```markdown
vehicle-allocation/ │ ├── app/ │ ├── main.py # FastAPI Entry Point │ ├── models.py # MongoDB Models │ ├── crud.py # CRUD Logic │ ├── schemas.py # Pydantic Schemas │ ├── utils.py # Utility Functions (like caching) │ ├── db.py # MongoDB Connection Logic │ ├── tests/ # Unit and Integration Tests │ └── test_allocations.py ├── Dockerfile # Docker Configuration ├── docker-compose.yml # MongoDB with FastAPI ├── requirements.txt # Dependencies └── README.md # Setup Instructions

## Setup

1. . Clone the repository:
   ```bash
   git clone <repo-url>
   cd vehicle-allocation

3. Run python -m venv venv 
4. Activate the virtual environment
4. If run locally then use following steps:
   ```bash
   pip install -r requirements.txt
   fastapi run .\app\main.py
   
  OR Build and run the Docker containers:
   ```bash
   docker-compose up --build

6. Access the app at http://localhost:8000/docs

Deployment Strategy
1. Use Docker for consistent environments.
2. Host on AWS EC2 or Azure App Services.
3. Use MongoDB Atlas for cloud-hosted MongoDB.
4. Set up CI/CD pipelines with GitHub Actions for automated deployment.
