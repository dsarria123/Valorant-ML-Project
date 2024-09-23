# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies specified in requirements.txt
# (You should create a requirements.txt file that lists Flask, boto3, and other dependencies)
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable (if you want to pass any)
# ENV FLASK_ENV=production

# Run app.py when the container launches
CMD ["python", "app.py"]
