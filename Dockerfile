# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install any required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (if the app runs on this port)
EXPOSE 5000

# Define the command to run the application
CMD ["python", "main.py"]
