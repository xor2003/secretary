# Use an official Python runtime as a parent image
FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install project dependencies from pyproject.toml
RUN pip install --no-cache-dir .

# Run app.py when the container launches
CMD ["python", "run.py"]