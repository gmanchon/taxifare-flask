
from Taxifare.data import get_data, get_data_from_gcp, clean_df
from Taxifare.gcp import upload_model_to_gcp
from Taxifare.transformers import DistanceTransformer
from Taxifare.utils import compute_rmse
from Taxifare.mlflow_base import MLFlowBase

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

import joblib

class Trainer(MLFlowBase):

    def __init__(self, params):

        experiment_name = '[FR] [Paris] [gmanchon] taxifare recap d3'
        mlflow_url = 'https://mlflow.lewagon.co/'

        # calling mother class init
        super().__init__(experiment_name, mlflow_url)

        # getting training parameters
        self.distance_type = params.get('distance', 'euclidian')
        self.model_type = params.get('model', 'randomforest')

        print(params)

    def create_pipeline(self):

        # create model depending on user choice
        if self.model_type == 'randomforest':
            model = RandomForestRegressor(n_estimators=100, max_depth=10, n_jobs=-1)
        elif self.model_type == 'linear':
            model = LinearRegression()

        # create pipeline
        steps = [('distance_transfo', DistanceTransformer(distance=self.distance_type)),
                ('scaler', StandardScaler()),
                ('model', model)]

        pipeline = Pipeline(steps=steps)

        return pipeline

    def train(self):

        # get data
        df = get_data() # get data from local disk
        # df = get_data_from_gcp() # get data from GCP
        df = clean_df(df)

        # get X and y
        cols = ["pickup_latitude",
                "pickup_longitude",
                "dropoff_latitude",
                "dropoff_longitude"]

        y = df["fare_amount"]
        X = df[cols]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

        # create pipeline
        self.model = self.create_pipeline()

        # create a mlflow run
        self.mlflow_create_run()

        # push params to mlflow
        self.mlflow_log_param('model', self.model_type)
        self.mlflow_log_param('distance', self.distance_type)

        # train
        self.model.fit(X_train, y_train)

        # predict
        y_pred = self.model.predict(X_test)

        # perf
        rmse = compute_rmse(y_pred, y_test)

        print(rmse)

        # determine the path to save the model to on GCP
        # linear/euclidian
        model_path = 'RF/{}/{}'.format(
            self.model_type,
            self.distance_type)

        # save model
        joblib.dump(self.model, 'model.joblib') # save data to local disk
        upload_model_to_gcp('model.joblib', model_path) # save data to GCP

        # push metrics to mlflow
        self.mlflow_log_metric('rmse', rmse)

if __name__ == '__main__':

    #
    # iterate on all combinations of training params
    #

    # iterate using combinations of params
    run_params = [
            ['linear', 'randomforest'], # model
            ['euclidian', 'manhattan'] # distance
        ]

    import itertools

    for index, element in enumerate(itertools.product(*run_params)):

        params = dict (
            model = element[0],
            distance = element[1]
        )

        trainer = Trainer(params)
        trainer.train()
