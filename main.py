from data_preprocessor import DataPreprocessor
from model_trainer import ModelTrainer
from dashboard import Dashboard
from cluster_model_trainer import ClusterModelTrainer

# Use relative path for the dataset
file_path = 'heart datasets/Metabolic Syndrome_Minhas Open data set.xlsx'

# Data Preprocessing
preprocessor = DataPreprocessor(file_path)
preprocessor.load_data()
preprocessor.impute_missing_values()
#preprocessor.scale_data()
processed_data = preprocessor.get_processed_data()

# Model Training
selected_features = ['Age', 'WaistCirc', 'BMI', 'BloodGlucose', 'HDL', 'Triglycerides']
trainer = ModelTrainer(selected_features)
trainer.prepare_data(processed_data)
trainer.train_model()
trainer.evaluate_model()

# Cluster Analysis
clustertrainer = ClusterModelTrainer(n_clusters=3)
clustertrainer.fit(trainer.X_train)

# Dashboard
dashboard = Dashboard(trainer, clustertrainer)
dashboard.layout()
dashboard.add_callbacks()
dashboard.run()