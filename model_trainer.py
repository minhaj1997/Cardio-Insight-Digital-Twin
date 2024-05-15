from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

class ModelTrainer:
    def __init__(self, selected_features, categorical_features):
        self.selected_features = selected_features
        self.categorical_features = categorical_features
        self.model = RandomForestClassifier(random_state=42)
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_importances = None

    def prepare_data(self, data):
        X = data[self.selected_features]
        y = data['MetabolicSyndrome']
        
        # Impute missing values with the median for continuous variables
        for column in self.selected_features:
            if X[column].isnull().any():
                X[column].fillna(X[column].median(), inplace=True)

        # Check again after imputation
        missing_values_after_imputation = X.isnull().sum()
        
        # If all missing values are handled, proceed to train the model again
        if not missing_values_after_imputation.any():
            
            for column in self.selected_features:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                self.X_train = X_train
                self.X_test = X_test
                self.y_train = y_train
                self.y_test = y_test

        """
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', 'passthrough', self.selected_features),
                ('cat', OneHotEncoder(), self.categorical_features)
            ]
        )
        self.X_train = preprocessor.fit_transform(self.X_train)
        self.X_test = preprocessor.transform(self.X_test)
        """

    def train_model(self):
        self.model.fit(self.X_train.values, self.y_train.values)
        self.feature_importances = self.model.feature_importances_

    def evaluate_model(self):
        y_pred = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred)
        recall = recall_score(self.y_test, y_pred)
        roc_auc = roc_auc_score(self.y_test, y_pred)
        conf_matrix = confusion_matrix(self.y_test, y_pred)

        return accuracy, precision, recall, roc_auc, conf_matrix
