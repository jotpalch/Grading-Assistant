# Grading Assistant

This Grading Assistant is a Python application designed to automatically grade C++ code submissions. It supports both on-time and late submissions, and it produces grading results in both JSON and CSV formats.

The application is designed to be run in a Docker container for consistent grading environments.

## Table of Contents

- [Getting Started](#getting-started)
- [Installation](#installation)
- [Setting Up Test Cases and Answers](setting-up0test-cases-and-answers)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Understanding the Results](understanding-the-results)

## Getting Started

To get started, you first need to have Docker installed on your machine. If you do not have Docker installed, you can download it here: https://docs.docker.com/get-docker/

Once Docker is installed, you can clone this repository to your local machine.

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/jotpalch/grading-assistant.git
```

### Setting Up Test Cases and Answers

1. Modify the directory `template` in the root of your project folder.

2. For each problem, create a sub-folder in the `template` directory. The sub-folder's name should be the problem's number/index (e.g., `1`, `2`, `3`).

3. Inside each problem's sub-folder, create two more sub-folders: `testcase` and `answer`.

4. Under the `testcase` folder, create input files for all the test cases. The input files should be named in the format `n.txt`, where `n` is the test case number (starting from 1).

5. Similarly, under the `answer` folder, create output files for all the test cases. The output files should match the corresponding input files and be named in the format `n.txt`.


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

## Understanding the Results

The results are presented per student, per problem, per test case. For example:

```json
{
    "student_id": {
        "late": false,
        "1": {
            "1": {
                "pass": true,
                "err": []
            },
            "2": {
                "pass": false,
                "err": ["Line 1: 'Output' != 'Expected'"]
            }
        }
    }
}
```

- `"late"`: Indicates if the submission was late.
- `"1"`: Problem number.
- Inside each problem, `"1"` and `"2"` are the test case numbers.
- `"pass"`: Indicates if the test case was passed.
- `"err"`: Contains error messages if the test case wasn't passed. If the test case was passed, this will be an empty array.

