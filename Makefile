
# bucket
BUCKET_NAME=le-wagon-data-gmanchon-batch-414

# training folder
BUCKET_TRAINING_FOLDER=trainings

# training params
REGION=europe-west1

# app environment
PYTHON_VERSION=3.7
FRAMEWORK=scikit-learn
RUNTIME_VERSION=1.15

# package params
PACKAGE_NAME=Taxifare
FILENAME=trainer

# pred
# PRED_FILENAME=predict

##### Job - - - - - - - - - - - - - - - - - - - - - - - - -

JOB_NAME=taxi_fare_training_pipeline_450_$(shell date +'%Y%m%d_%H%M%S')

run_locally:
	python -m Taxifare.trainer

gcp_submit_training:
	gcloud ai-platform jobs submit training ${JOB_NAME} \
		--job-dir gs://${BUCKET_NAME}/${BUCKET_TRAINING_FOLDER} \
		--package-path ${PACKAGE_NAME} \
		--module-name ${PACKAGE_NAME}.${FILENAME} \
		--python-version=${PYTHON_VERSION} \
		--runtime-version=${RUNTIME_VERSION} \
		--config config.yaml \
		--region ${REGION} \
		--stream-logs

predict:
	python ${PRED_FILENAME}.py
