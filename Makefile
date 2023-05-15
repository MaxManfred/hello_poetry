#PROJECT_ID ?= <CHANGEME>
#REGION ?= <CHANGEME>
#PROJECT_NUMBER ?= $$(gcloud projects list --filter=${PROJECT_ID} --format="value(PROJECT_NUMBER)")
#CODE_BUCKET ?= serverless-spark-code-repo-${PROJECT_NUMBER}
#TEMP_BUCKET ?= serverless-spark-staging-${PROJECT_NUMBER}
#DATA_BUCKET ?= serverless-spark-data-${PROJECT_NUMBER}
PYTHON_VERSION ?= 3.10.11
APP_NAME ?= $$(cat pyproject.toml| grep name | cut -d" " -f3 | sed  's/"//g')
VERSION_NO ?= $$(poetry version --short)
SRC_WITH_DEPS ?= src_with_deps

.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))

.DEFAULT_GOAL := help

help: ## This is help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## CleanUp Prior to Build
	@rm -Rf ./dist

build: clean ## Build Python Package with Dependencies
	@echo "Packaging Code and Dependencies for ${APP_NAME}-${VERSION_NO}"
	@mkdir -p ./dist
	@poetry update
#	@poetry export -f requirements.txt --without-hashes -o requirements.txt
#	@poetry run pip install . -r requirements.txt -t ${SRC_WITH_DEPS}
#	@cd ./${SRC_WITH_DEPS}
#	@find . -name "*.pyc" -delete
#	@cd ./${SRC_WITH_DEPS} && zip -x "*.git*" -x "*.DS_Store" -x "*.pyc" -x "*/*__pycache__*/" -x ".idea*" -r ../dist/${SRC_WITH_DEPS}.zip .
#	@rm -Rf ./${SRC_WITH_DEPS}
#	@rm -f requirements.txt
	@cp ./spark/runner.py ./dist
	@cp ./scripts/init_actions.sh ./dist
	@poetry build
#	@mv ./dist/${SRC_WITH_DEPS}.zip ./dist/${APP_NAME}_${VERSION_NO}.zip
#	@gsutil cp -r ./dist gs://${CODE_BUCKET}

#deploy_local: build ## Create and activate a virtual environment and install the Spark App
#	@pyenv virtualenv test-deployment
#	@pyenv activate test-deployment
#	@pip install --force-reinstall --no-cache-dir dist/hello_poetry-0.1.0-py3-none-any.whl
#
#run_local: deploy_local ## Execute the locally deployed Spark App
#	@python -m hello_poetry.sample_job
#
#undeploy_local: ## Deactivate and delete the virtualenv for testing deployment
#	@pyenv deactivate
#	@pyenv uninstall ${PYTHON_VERSION}/envs/test-deployment
