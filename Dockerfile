# Use the official Python image from the Docker Hub
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements file first, so dependencies can be cached
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 8080 available outside this container
EXPOSE 8080

# Run main.py when the container launches
CMD ["python", "main.py"]
