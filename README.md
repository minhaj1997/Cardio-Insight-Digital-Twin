# Digital Shadow

A digital shadow application for cardiovascular health monitoring and risk assessment. This application uses machine learning to analyze patient data and provide real-time insights into metabolic syndrome risk factors.

## Features

- Real-time patient health monitoring
- Metabolic syndrome risk assessment
- Interactive dashboard with health metrics visualization
- Patient data clustering for risk categorization
- Historical patient data tracking
- Docker containerization for easy deployment
- REST API for patient data upload

## Project Structure

```
.
├── dashboard.py              # Main dashboard application
├── main.py                   # Application entry point
├── model_trainer.py          # Machine learning model training
├── cluster_model_trainer.py  # Clustering model for risk categorization
├── data_preprocessor.py      # Data preprocessing utilities
├── patient_service.py        # Patient data service
├── connection.py            # Database connection handler
├── routes.py                # API routes
├── digital_twin_patient.sql # Database schema
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
└── docker-compose.yml      # Docker Compose configuration
```

## Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose
- MySQL 8.0

## Installation

### Docker Deployment

These steps assume you are on a machine with Docker and have cloned the repository.

1.  **Navigate to Project Directory**
    Make sure you are in the root directory of the project.

2.  **Check Dataset**
    Ensure the `heart datasets` directory exists and contains the required `.xlsx` file.

3.  **Build and Run with Docker Compose**
    This single command will build the Docker images for the services and start the containers. The `--build` flag ensures that the images are rebuilt if there are any changes to the source code or `Dockerfile`.
    ```bash
    docker-compose up --build
    ```
    Your application (dashboard) and database will now be running.

## Accessing the Application
- **Dashboard**: `http://localhost:8050`
- **API Base URL**: `http://localhost:5001`

## API Usage

### Running the API Server

After starting the Docker containers, run the API server in a new terminal:
```bash
docker exec -it codefiles-app-1 python routes.py
```

### API Endpoints

#### Upload Patient Record
- **URL**: http://localhost:5001/api/upload_patient_record
- **Method**: POST
- **Headers**: 
  - Content-Type: application/json
- **Body**:
```json
{
    "Age": 45,
    "WaistCirc": 90,
    "BMI": 25.5,
    "BloodGlucose": 120,
    "HDL": 45,
    "Triglycerides": 150
}
```

## Usage

1. The dashboard will automatically load the latest patient data
2. View real-time health metrics and risk assessments
3. Navigate between different views using the navigation links
4. Monitor health alerts and risk factors
5. View historical patient data in the past patients section
6. Use the API to upload new patient records

## Stopping the Application

To stop the application, press `Ctrl+C` in the terminal or run:
```bash
docker-compose down
```

## Troubleshooting

- If port 8050 is already in use, you can modify the port in `docker-compose.yml`
- If port 5001 is already in use, you can modify the port in `docker-compose.yml`
- Make sure the dataset file is in the correct location: `heart datasets/Metabolic Syndrome_Minhas Open data set.xlsx`
- If the API container name is different, use `docker ps` to check the correct container name

## Contact

Minhaj Siddiqui - [@minhaj1997](https://github.com/minhaj1997)

Project Link: [https://github.com/minhaj1997/Cardio-Insight-Digital-Twin](https://github.com/minhaj1997/Cardio-Insight-Digital-Twin) 
