# Cardio Insight Digital Twin

## Running the Application on a New System

### Prerequisites
- Docker installed on the system
- Docker Compose installed on the system

### Required Files
1. `cardio-insight-app.tar` (Docker image)
2. `docker-compose.yml`
3. `digital_twin_patient.sql`
4. `heart datasets` directory containing the dataset file

### Steps to Run

1. Create a project directory:
```bash
mkdir cardio-insight
cd cardio-insight
```

2. Place all required files in the directory:
   - Copy `cardio-insight-app.tar`
   - Copy `docker-compose.yml`
   - Copy `digital_twin_patient.sql`
   - Copy the `heart datasets` directory

3. Load the Docker image:
```bash
docker load < cardio-insight-app.tar
```

4. Start the application:
```bash
docker-compose up
```

5. Access the application:
   - Open your web browser
   - Go to http://localhost:8050

### Stopping the Application
To stop the application, press `Ctrl+C` in the terminal or run:
```bash
docker-compose down
```

### Troubleshooting
- If port 8050 is already in use, you can modify the port in `docker-compose.yml`
- If port 3307 is already in use, you can modify the MySQL port in `docker-compose.yml`
- Make sure the dataset file is in the correct location: `heart datasets/Metabolic Syndrome_Minhas Open data set.xlsx` 