from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class ClusterModelTrainer:
    def __init__(self, n_clusters):
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()
        self.cluster_centers = None

    def fit(self, X):
        # Fit the scaler on the training data
        X_scaled = self.scaler.fit_transform(X.values)
        # Fit the KMeans model on the scaled data
        self.kmeans.fit(X_scaled)
        self.cluster_centers = self.kmeans.cluster_centers_

    def predict(self, X):
        # Scale the input data using the same scaler
        X_scaled = self.scaler.transform(X.values)
        return self.kmeans.predict(X_scaled)

