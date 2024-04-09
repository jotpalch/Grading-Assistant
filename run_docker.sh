#!/bin/bash

# Make the script executable
# chmod +x run_docker.sh

mkdir -p result
mkdir -p code_backup

# put the code download from e3 in the folder
mkdir -p code
mkdir -p code_late

pause 'Put the code download from e3 in the folder code and code_late. Press [Enter] key to continue...'

# Get the current directory
current_dir=$(pwd)

# Build the Docker image
docker build -t gradingsystem .

# Run the Docker container
docker run \
    -v $current_dir/code:/app/code \
    -v $current_dir/code_late:/app/code_late \
    -v $current_dir/template:/app/template \
    -v $current_dir/result:/app/result \
    -v $current_dir/code_backup:/app/code_backup \
    -it --rm gradingsystem