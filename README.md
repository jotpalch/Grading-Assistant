# Grading Assistant

This Grading Assistant is a Python application designed to automatically grade C++ code submissions and check for plagiarism using MOSS (Measure of Software Similarity). It supports both on-time and late submissions, and it produces grading results in both JSON and CSV formats.

The application is designed to be run in a Docker container for consistent grading environments.

## Table of Contents

- [Getting Started](#getting-started)
- [Installation](#installation)
- [Setting Up Test Cases and Answers](#setting-up-test-cases-and-answers)
- [Usage](#usage)
- [MOSS Plagiarism Check](#moss-plagiarism-check)
- [File Structure](#file-structure)
- [Understanding the Results](#understanding-the-results)

## Getting Started

To get started, you first need to have Docker installed on your machine. If you do not have Docker installed, you can download it here: https://docs.docker.com/get-docker/

Once Docker is installed, you can clone this repository to your local machine.

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/jotpalch/grading-assistant.git
```

## Setting Up Test Cases and Answers

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

## MOSS Plagiarism Check

1. Run the `run_moss.sh` shell script to start the plagiarism check using MOSS.

```bash
chmod +x run_moss.sh
./run_moss.sh
```

2. You will be prompted to enter your MOSS userid. After entering the userid, the script will automatically send all C++ files in the `code_backup` directory to MOSS for plagiarism check.

3. The plagiarism report URLs for each problem will be printed on the console and also appended to the `report.txt` file.


### Applying for a MOSS User ID

Moss is a command-line script that sends your program files to a server for plagiarism detection. You provide the moss script with criteria, such as the programming language, and then it sends off the files. You are then returned a link where you can view the results.

To get started with Moss, you need to register for it. Here's how you can do it:

1. Visit the [Moss website](http://theory.stanford.edu/~aiken/moss/), and navigate to the "Register for Moss" section. If you're having trouble understanding the instructions on the website, here's a simplified version:

2. Send an email to moss@moss.stanford.edu with the following content:

    ```
    registeruser
    mail username@domain
    ```
    Replace `your-email@your-institution.edu` with your academic email address. It's important to use **your academic email address** (the one associated with your institution) as MOSS is a service for academic use.

3. After some time, you will receive an email that contains a moss script with a unique user id just for you. This is a Perl script, so ensure that your system can run Perl programs.

Remember to keep your user id confidential and do not share it with others. You will need this user id to run the Moss checks.

## File Structure

- `run_docker.sh`: A shell script to pull and run the Docker image.
- `run_moss.sh`: A shell script to run the MOSS plagiarism check.
- `main.py`: The main Python script that handles grading.
- `moss_check.py`: The Python script that handles MOSS plagiarism check.
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
