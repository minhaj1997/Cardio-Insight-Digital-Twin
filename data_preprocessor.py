import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

class DataPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.numerical_cols = ['Age', 'Income', 'WaistCirc', 'BMI', 'UrAlbCr', 'UricAcid', 'BloodGlucose', 'HDL', 'Triglycerides']
        self.categorical_cols =  ['Sex', 'Marital']

    def load_data(self):
        self.data = pd.read_excel(self.file_path)
    
    def impute_missing_values(self):
        imputer_num = SimpleImputer(strategy='median')
        imputer_cat = SimpleImputer(strategy='most_frequent')

        self.data[self.numerical_cols] = imputer_num.fit_transform(self.data[self.numerical_cols])
        self.data[self.categorical_cols] = imputer_cat.fit_transform(self.data[self.categorical_cols])

    def scale_data(self):
        scaler = StandardScaler()
        numerical_cols = ['Age', 'Income', 'WaistCirc', 'BMI', 'UrAlbCr', 'UricAcid', 'BloodGlucose', 'HDL', 'Triglycerides']
        self.data[numerical_cols] = scaler.fit_transform(self.data[numerical_cols])

    def get_processed_data(self):
        return self.data


