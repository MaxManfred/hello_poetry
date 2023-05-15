Useful links

https://medium.com/lambda-automotive/python-poetry-finally-easy-build-and-deploy-packages-e1e84c23401f
https://python-poetry.org/docs/cli/
https://python-poetry.org/docs/basic-usage/

To build wheel
- make build

To create and activate test deployment venv:
- pyenv virtualenv test-deployment
- pyenv activate test-deployment

To install Spark app (forcing re-installation):
- pip install --force-reinstall --no-cache-dir dist/hello_poetry-0.1.0-py3-none-any.whl

To test the Spark app:
- python
- execute commands in the shell
  or
- python -m hello_poetry.sample_job

To deactivate and remove venv:
- pyenv deactivate
- pyenv uninstall 3.10.11/envs/test-deployment

To delete the build artifacts:
- rm -fr dist

GCP

Before starting this part, make sure you've run make build command

- create a bucket (for instance training-386309)
- upload the following files into the root (do not copy the intermediate folders):
    - dist/runner.py
    - dist/init_actions.sh
    - dist/hello_poetry-0.1.0-py3-none-any.whl
    - dist/hello_airflow.py
- start a Dataproc cluster using the following command from a Cloud Shell:

  gcloud dataproc clusters create training-cluster \
  --autoscaling-policy training-autoscaling-policy \
  --enable-component-gateway \
  --region europe-west8 \
  --zone europe-west8-a \
  --master-machine-type e2-standard-2 \
  --master-boot-disk-size 500 \
  --num-workers 2 \
  --worker-machine-type e2-standard-2 \
  --worker-boot-disk-size 500 \
  --image-version 2.1-ubuntu20 \
  --optional-components JUPYTER \
  --initialization-actions 'gs://training-386309/init_actions.sh' \
  --project training-386309

- SSH into master node or any worker node to check the Spark App has been installed using the command
  pip freeze | grep poetry

Submit a Dataproc job type the following command in a Cloud Shell
gcloud dataproc jobs submit pyspark gs://training-386309/runner.py --cluster=training-cluster --region=europe-west8 -- runner=gs://training-386309/people.parquet temporary_view=people gender=M
and check the Dataproc Jobs page to see the job logs

TODO: DESCRIBE HOW TO CREATE CLOUD COMPOSER ENVIRONMENT PROGRAMMATICALLY


Upload the Cloud Composer DAG to the DAG folder using (from a Cloud Shell)
gcloud composer environments storage dags import \
--environment example-environment \
--location europe-west6 \
--source gs://training-386309/hello_airflow.py


