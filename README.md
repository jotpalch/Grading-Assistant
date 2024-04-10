# Grading Assistant

This Grading Assistant is a Python application designed to automatically grade C++ code submissions. It supports both on-time and late submissions, and it produces grading results in both JSON and CSV formats.

The application is designed to be run in a Docker container for consistent grading environments.

## Table of Contents

- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)

## Getting Started

To get started, you first need to have Docker installed on your machine. If you do not have Docker installed, you can download it here: https://docs.docker.com/get-docker/

Once Docker is installed, you can clone this repository to your local machine.

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/jotpalch/grading-assistant.git
```

## Usage

1. Run the `run_docker.sh` shell script to set up the environment and run the Grading Assistant. 

```bash
cd grading-assistant
chmod +x run_docker.sh
./run_docker.sh
```

2. When prompted, put the code downloaded from e3 in the `code` and `code_late` folders. 

3. The Grading Assistant will execute the `main.py` script, which extracts C++ files from the submitted zip files and grades them based on provided test cases. 

4. The grading results will be stored in the `result` directory in both JSON and CSV formats. A backup of the graded code will be saved in the `code_backup` directory. 

## File Structure

- `run_docker.sh`: A shell script to pull and run the Docker image.
- `main.py`: The main Python script that handles grading.
- `code` and `code_late`: Directories for on-time and late code submissions.
- `result`: Directory for storing grading results.
- `code_backup`: Directory for storing backups of graded code.

