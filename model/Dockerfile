# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY model/ .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Make port 6969 available to the world outside this container
EXPOSE 6969

# Run endpoint.py when the container launches
CMD ["python", "/app/inference/endpoint.py"]
