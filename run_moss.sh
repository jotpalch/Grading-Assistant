#!/bin/bash

# Make the script executable
# chmod +x run_moss.sh

# Define the directory where the C++ files are stored
CODE_DIRECTORY="./code_backup/"

# Check if the directory exists
if [ ! -d "$CODE_DIRECTORY" ]; then
    echo "Directory $CODE_DIRECTORY does not exist."
    exit 1
fi

# Get the user id
echo -n "Enter your MOSS userid and press [ENTER]: "
read userid

# Check if the user id is empty
if [ -z "$userid" ]; then
    echo "You must enter a userid."
    exit 1
fi

# pull the docker image
docker pull ghcr.io/jotpalch/grading-assistant:latest

# Run the MOSS script
docker run -v $(pwd)/code_backup:/app/code_backup -w /app ghcr.io/jotpalch/grading-assistant:latest python run_moss.py $userid
