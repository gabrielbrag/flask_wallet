# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the api_ebanx directory contents into the container at /app/api_ebanx
COPY api_ebanx /app/api_ebanx

# Copy the tests directory contents into the container at /app/test
COPY test /app/test

# Copy the requirements.txt file from the api_ebanx directory to /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ensure pytest is installed
RUN pip install pytest

# Set environment variables for PYTHONPATH
ENV PYTHONPATH=/app/api_ebanx

# Set the entrypoint to run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "api_ebanx.app:app"]