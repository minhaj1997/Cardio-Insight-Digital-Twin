from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
import os
import time
from sqlalchemy.exc import OperationalError

# Get database configuration from environment variables
DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
DB_USER = os.getenv('MYSQL_USER', 'root')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Minhajsiddiqui@1997')
DB_NAME = os.getenv('MYSQL_DATABASE', 'digitaltwin')

# SQLAlchemy engine creation
database_url = f"mysql+pymysql://{DB_USER}:{quote(DB_PASSWORD)}@{DB_HOST}:3306/{DB_NAME}"
engine = create_engine(database_url, echo=True)

# Function to test database connection with retries
def wait_for_db(max_retries=5, retry_interval=5):
    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
                print("MySQL Database connection successful")
                return True
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Database connection attempt {attempt + 1} failed. Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                print(f"Failed to connect to database after {max_retries} attempts")
                raise e

# Wait for database to be ready
wait_for_db()

# Reflect an existing database into a new model
metadata = MetaData()
metadata.reflect(engine)

# Access the 'patient' table
patient_table = metadata.tables['patient']

# Create a session
Session = sessionmaker(bind=engine)


