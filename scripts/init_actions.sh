#!/bin/bash

gsutil cp gs://training-386309/hello_poetry-0.1.0-py3-none-any.whl .
echo "Spark App whl file copied locally from GCS!"

pip install --force-reinstall --no-cache-dir hello_poetry-0.1.0-py3-none-any.whl
echo "Spark App installed!"