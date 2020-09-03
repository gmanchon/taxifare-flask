
import pandas as pd
from google.cloud import storage

from Taxifare.params import BUCKET_NAME, BUCKET_TRAIN_DATA_PATH

def get_data():
    url = "s3://wagon-public-datasets/taxi-fare-train.csv"
    df = pd.read_csv(url, nrows=100)
    return df

def get_data_from_gcp():

    data_file = 'data/data_from_gcp.csv'

    client = storage.Client().bucket(BUCKET_NAME)

    blob = client.blob(BUCKET_TRAIN_DATA_PATH)

    blob.download_to_filename(data_file)

    df = pd.read_csv(data_file)
    return df

def clean_df(df):
    df = df.dropna(how='any', axis='rows')
    df = df[(df.dropoff_latitude != 0) | (df.dropoff_longitude != 0)]
    df = df[(df.pickup_latitude != 0) | (df.pickup_longitude != 0)]
    if "fare_amount" in list(df):
        df = df[df.fare_amount.between(0, 4000)]
    df = df[df.passenger_count < 8]
    df = df[df.passenger_count >= 0]
    df = df[df["pickup_latitude"].between(left=40, right=42)]
    df = df[df["pickup_longitude"].between(left=-74.3, right=-72.9)]
    df = df[df["dropoff_latitude"].between(left=40, right=42)]
    df = df[df["dropoff_longitude"].between(left=-74, right=-72.9)]
    return df
