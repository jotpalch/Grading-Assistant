# Use an official Python runtime as a parent image
FROM python:latest

# Install g++ for compiling C++ code
RUN apt-get update && \
    apt-get install -y g++ && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]