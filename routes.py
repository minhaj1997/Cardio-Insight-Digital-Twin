from flask import Flask, request, jsonify
import pandas as pd
from patient_service import insert_patient

app = Flask(__name__)


@app.route('/api/upload_patient_record', methods=['POST'])
def upload_health_data():
    data = request.json
    if not data:
        return jsonify(status="error", message="No data provided"), 400
    
    required_fields = ['Age', 'WaistCirc', 'BMI', 'BloodGlucose', 'HDL', 'Triglycerides']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify(status="error", message="Missing fields: " + ", ".join(missing_fields)), 400
    
    try:
        data['Age'] = int(data['Age'])
        data['WaistCirc'] = float(data['WaistCirc'])
        data['BMI'] = float(data['BMI'])
        data['BloodGlucose'] = float(data['BloodGlucose'])
        data['HDL'] = float(data['HDL'])
        data['Triglycerides'] = float(data['Triglycerides'])
    except ValueError as e:
        return jsonify(status="error", message="Invalid data format"), 400
    
    
    try:
        insert_patient(data)
        return jsonify(status="success", message="Data received successfully")
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
