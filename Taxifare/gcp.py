
from Taxifare.params import BUCKET_NAME, MODEL_BASE_PATH

from google.cloud import storage

def upload_model_to_gcp(local_model_filename, gcp_model_path):

    # models/taxifare_450/.../model.joblib
    storage_location = 'models_450/{}/{}/{}'.format(
        MODEL_BASE_PATH,
        gcp_model_path,
        'model.joblib')

    client = storage.Client().bucket(BUCKET_NAME)

    blob = client.blob(storage_location)

    blob.upload_from_filename(local_model_filename)
