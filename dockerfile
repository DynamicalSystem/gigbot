# syntax=docker/dockerfile:1
FROM python:3.11-alpine

# pass in the following build arguments from the docker build command
ARG ENV
ARG CONTAINER_FOLDER
ARG HOST_FOLDER

# Set the working directory
WORKDIR /code
RUN mkdir -p dist

# Install dependencies
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
COPY requirements_local.txt requirements_local.txt
COPY dist/* dist/

# Install the publisher package
RUN python -m pip install --upgrade build pip setuptools wheel
RUN python -m pip install -r requirements.txt
RUN python -m pip install -r requirements_local.txt

# Set environment variables from makefile
RUN echo "Environment: ${ENV}"
RUN echo "Container folder: ${CONTAINER_FOLDER}"
RUN echo "Host folder: ${HOST_FOLDER}"
ENV DYNAMICAL_SYSTEM_ENVIRONMENT=${ENV}
ENV DYNAMICAL_SYSTEM_FOLDER=${HOST_FOLDER}
ENV CONTAINER_FOLDER=${CONTAINER_FOLDER}

# Create the container folder(s)
RUN mkdir -p ${CONTAINER_FOLDER}/config

# Copy the source code
COPY . .

# Run the module
CMD ["gigbot"]
