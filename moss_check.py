import os
import sys
import mosspy

def main():
    # Check if the user has provided a user id
    if len(sys.argv) != 2:
        print("Usage: python moss_check.py <userid>")
        sys.exit(1)

    # Get the user id from the command line arguments
    userid = sys.argv[1]

    # Initialize the Moss object with the user id and language
    m = mosspy.Moss(userid, "cc")

    # Define the directory where the C++ files are stored
    code_directory = "./code_backup/"

    # Iterate over the directories in the code directory
    for problem_dir in sorted(os.listdir(code_directory)):
        problem_path = os.path.join(code_directory, problem_dir)

        # Add each C++ file in the current directory to the Moss object
        for file in os.listdir(problem_path):
            if file.endswith(".cpp"):
                file_path = os.path.join(problem_path, file)
                try:
                    m.addFile(file_path)
                except Exception as e:
                    print(f"Failed to add file {file_path} due to error: {str(e)}")
                    continue

        # Send the files to Moss and get the report URL
        url = m.send()

        print(f"Report Url for problem {problem_dir}: {url}")

        # Append the report URL to the report file
        with open("report.txt", "a") as f:
            f.write(f"Problem {problem_dir}: {url}\n")

if __name__ == "__main__":
    main()
