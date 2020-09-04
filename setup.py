from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
    # flask
    'Flask==1.1.1',
    'Flask-Cors==3.0.8',
    'gunicorn==20.0.4',
    # training
    'numpy==1.18.4',
    'pandas==0.24.2',
    'scikit-learn==0.20.4',
    'joblib==0.14.1',
    # tracking
    'memoized-property==1.0.3',
    'mlflow==1.8.0',
    # storage
    's3fs==0.4.2',
    'gcsfs==0.6.0',
    'google-cloud-storage==1.26.0',
    # logs
    'termcolor==1.1.0']

setup(
    name='TaxiFareModel450',
    version='1.0',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='Taxi Fare Prediction Pipeline 450'
)
