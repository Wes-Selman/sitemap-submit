# Use the official Python image from the Docker Hub
FROM python:alpine
# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available outside this container
EXPOSE 8000

# Run main.py when the container launches
CMD ["python", "main.py"]