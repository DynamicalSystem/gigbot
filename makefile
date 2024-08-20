# Makefile
ENV ?= test

NAMESPACE := dynamicalsystem
PACKAGE_NAME := gigbot
TARBALL := ${NAMESPACE}_${PACKAGE_NAME}.tar.gz
HOST_FOLDER := ${HOME}/.local/share
CONTAINER_FOLDER := /${NAMESPACE}.${PACKAGE_NAME}

all: clean build

# Prepare the build environment
build:
	pip install --upgrade build
	pip install --upgrade twine
	pip install --upgrade setuptools
	pip freeze > requirements.txt
	black .

	# Create the dist folder
	python3 -m build .

# Create and push a tarball for production
production: clean build
	@echo ${TARBALL}
	tar czvf $(TARBALL) dockerfile makefile requirements.txt requirements_local.txt dist config/prod.env docker-compose.yml
	cp $(TARBALL) "/Volumes/Dynamical System’s Public Folder/Drop Box/${NAMESPACE}"
	@echo run 'tar -xzf ${TARBALL}.tar.gz' on the prod server to extract the tarball
	@echo then run 'make deploy ENV=prod' to deploy the app

deploy:
	@echo Folder ${HOST_FOLDER}
	@echo Container Folder ${CONTAINER_FOLDER}
	@echo Namespace ${NAMESPACE}
	@echo Package ${PACKAGE_NAME}
	@echo Environment ${ENV}
	cp config/${ENV}.env ${HOST_FOLDER}/${NAMESPACE}.${PACKAGE_NAME}/config
	docker build \
		--build-arg ENV=${ENV} \
		--build-arg CONTAINER_FOLDER=${CONTAINER_FOLDER} \
		--build-arg HOST_FOLDER=${HOST_FOLDER} \
		-t ${NAMESPACE}/${PACKAGE_NAME} .

	export HOST_FOLDER=${HOST_FOLDER} && \
	echo $$HOST_FOLDER && \
	docker compose -f docker-compose.yml up -d

# Clean up build artifacts
clean:
	rm ${TARBALL} || true
	rm -fr dist
	find . -type d -name "*.egg-info" -exec rm -rf + || true

# Phony targets
.PHONY:
	all dist deploy docker-build clean prep production
