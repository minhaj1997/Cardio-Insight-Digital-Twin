from sqlalchemy import insert, desc
from connection import patient_table, Session


def insert_patient(data):
    session = Session()
    # Insert data statement using ORM dictionary unpacking
    new_patient = patient_table.insert().values(
        name=data['Name'],  # Make sure to include this if you've added a name column
        age=data['Age'],
        waist_circ=data['WaistCirc'],
        bmi=data['BMI'],
        blood_glucose=data['BloodGlucose'],
        hdl=data['HDL'],
        triglycerides=data['Triglycerides']
    )

    try:
        session.execute(new_patient)
        session.commit()
        print("Data inserted successfully.")
    except Exception as e:
        session.rollback()  # Rollback the changes on error
        print(f"Failed to insert data: {e}")
    finally:
        session.close()  # Close the session to free resources
        

def get_latest_patient():
    session = Session()
    try:
        # Assuming 'id' is the primary key that increments
        latest_patient = session.execute(
            patient_table.select().order_by(desc(patient_table.c.id)).limit(1)
        ).fetchone()  # fetchone() to get only the latest record

        return latest_patient if latest_patient else None  # Return the latest patient or None if no records
    except Exception as e:
        print(f"Error retrieving the latest patient: {e}")
        return None
    finally:
        session.close()
        
def fetch_all_patients():
    session = Session()
    try:
        # Fetch all patient records
        all_patients = session.execute(
            patient_table.select().order_by(patient_table.c.id)
        ).fetchall()  # fetchall() to get all records

        return all_patients
    except Exception as e:
        print(f"Error retrieving all patients: {e}")
        return []
    finally:
        session.close()
        
def fetch_patient_data_by_id(patient_id):
    session = Session()
    try:
        patient = session.execute(
            patient_table.select().where(patient_table.c.id == patient_id)
        ).fetchone()
        return patient
    finally:
        session.close()
        

