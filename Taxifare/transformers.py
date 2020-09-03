
from Taxifare.distance import minkowski_distance

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

class DistanceTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, distance='euclidian'):
        self.distance = distance

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)

        X = X.copy()

        if self.distance == "euclidian":
            X["distance"] = minkowski_distance(X, p=2) # euclidian
        elif self.distance == "manhattan":
            X["distance"] = minkowski_distance(X, p=1) # manhattan

        return X[["distance"]]

    def fit(self, X, y=None):
        return self
