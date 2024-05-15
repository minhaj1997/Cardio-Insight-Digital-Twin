from sklearn.cluster import KMeans

class ClusterModelTrainer:
    def __init__(self, n_clusters):
        self.kmeans = KMeans(n_clusters=n_clusters)
        self.cluster_centers = None

    def fit(self, X):
        self.kmeans.fit(X.values)
        self.cluster_centers = self.kmeans.cluster_centers_

    def predict(self, X):
        return self.kmeans.predict(X)
