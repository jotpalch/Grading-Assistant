import subprocess
import traceback
import zipfile
import shutil
import json
import sys
import os
import glob

TIME_LIMIT = 20
LATE_PENALTY = 0.8
SUBMISSION_FOLDER_PATH = './code'
LATE_SUBMISSION_FOLDER_PATH = './code_late'


def extract_cpp_files(zip_path, extract_path):
    """Extract C++ files from given zip file to specified path."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for zip_info in zip_ref.infolist():
            if zip_info.is_dir() or not zip_info.filename.endswith('.cpp') or '__MACOSX' in zip_info.filename:
                continue
            zip_info.filename = os.path.basename(zip_info.filename)
            zip_ref.extract(zip_info, extract_path)


class Grader:
    """A class to handle grading operations."""
    
    def __init__(self, submission_folder_path, late_submission_folder_path):
        self.submission_folder_path = submission_folder_path
        self.late_submission_folder_path = late_submission_folder_path

    def grading(self, extract_folder_path, late=False):
        """Grade the extracted code files."""
        result_dict = {}
        num_students = len(os.listdir(extract_folder_path))

        for i, student_folder_path in enumerate(os.listdir(extract_folder_path)):
            zip_file_path = os.listdir(os.path.join(extract_folder_path, student_folder_path))[0]

            student_id = zip_file_path.split('.')[0]
            num_problems = len(os.listdir('./template'))

            result_dict[student_id] = {"late": late}

            print(f"[{i+1:{3}}/{num_students}] Grading {student_id}")

            try:
                # Unzip the file
                extract_cpp_files(os.path.join(os.getcwd(), extract_folder_path, student_folder_path, zip_file_path), f"./out/{student_id}")
            except:
                print("Error while unzip the file")
                continue

            # Run the grading script
            for index_problem in range(1, num_problems+1):
                self.grade_problem(index_problem, result_dict, student_id)
                self.cp_files(index_problem, student_id)
                

            # clear files in out folder
            if os.path.exists(f"./out/{student_id}"):
                shutil.rmtree(f"./out/{student_id}")

        return result_dict
    
    def cp_files(self, index_problem, student_id):
        """Copy the files to the respective folder."""
        if not os.path.exists(f'./out/{student_id}/{index_problem}.cpp'):
            return

        if not os.path.exists(f'./code_backup/{index_problem}'):
            os.makedirs(f'./code_backup/{index_problem}')

        src_dir = f'./out/{student_id}/{index_problem}.cpp'
        dst_dir = f'./code_backup/{index_problem}/{student_id}_{index_problem}.cpp'

        shutil.copy(src_dir,dst_dir)

    def grade_problem(self, index_problem, result_dict, student_id):
        """Grade a specific problem for a specific student."""
        if not os.path.exists(f'./out/{student_id}/{index_problem}.cpp'):
            if os.path.exists(f'./out/{student_id}/{index_problem}.cpp.cpp'):
                os.rename(f'./out/{student_id}/{index_problem}.cpp.cpp', f'./out/{student_id}/{index_problem}.cpp')
            else:
                return

        result_dict[student_id][index_problem] = {}

        # compile the file
        p = subprocess.Popen(["g++", "-std=c++17", f"./out/{student_id}/{index_problem}.cpp", "-o", f"./out/{student_id}/{index_problem}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()

        if error:
            result_dict[student_id][index_problem] = {"err": "Compile error: " + error.decode('utf-8')}
            return

        # check if the number of testcase is the same as answer
        if len(os.listdir(f"./template/{index_problem}/testcase")) != len(os.listdir(f"./template/{index_problem}/answer")):
            print(f"Testcase and answer for {index_problem} is not the same")
            sys.exit(1)

        num_testcases = len(os.listdir(f"./template/{index_problem}/testcase"))

        # input the testcase
        for testcase in range(num_testcases):
            self.grade_testcase(index_problem, result_dict, student_id, testcase)

    def grade_testcase(self, index_problem, result_dict, student_id, testcase):
        """Grade a specific testcase for a specific problem and student."""
        result_dict[student_id][index_problem][testcase+1] = {"pass": True, "err": []}

        # Adjust the path to use .txt instead of .in or .out for the input and output files
        input_path = f'./template/{index_problem}/testcase/{testcase+1}.txt'
        output_path = f'./out/{student_id}/{index_problem}_output_{testcase+1}.txt'
        answer_path = f'./template/{index_problem}/answer/{testcase+1}.txt'

        # Replace the extension of input and output files if necessary
        if not os.path.exists(input_path):
            input_path = input_path.replace('.txt', '.in')
        if not os.path.exists(answer_path):
            answer_path = answer_path.replace('.txt', '.out')

        # set timeout 
        try:
            with open(input_path, 'r') as input_file, open(output_path, 'w') as output_file:
                p = subprocess.Popen(f'./out/{student_id}/{index_problem}', stdin=input_file, stdout=output_file)
                p.communicate(timeout=TIME_LIMIT)
        except Exception as e:
            # kill process if timeout
            p.kill()
            outs, errs = p.communicate()

            result_dict[student_id][index_problem][testcase+1]["pass"] = False
            result_dict[student_id][index_problem][testcase+1]["err"] = ["TLE"]
            return

        with open(output_path, 'r') as output_file, open(answer_path, 'r') as answer_file:
            try:
                output = output_file.readlines()
                answer = answer_file.readlines()
            except:
                result_dict[student_id][index_problem][testcase+1]["pass"] = False
                result_dict[student_id][index_problem][testcase+1]["err"] = ["invalid output file"]

        tmp_err_list = []
        for line, (out, ans) in enumerate(zip(output, answer)):
            if out != ans:
                err_str = f"Line {line+1}: {repr(out)} != {repr(ans)}"
                if len(err_str) > 250:
                    tmp_err_list.append(f"Line {line+1}: ...")
                else:
                    tmp_err_list.append(err_str)

        if len(output) == 0:
            result_dict[student_id][index_problem][testcase+1]["pass"] = False
            result_dict[student_id][index_problem][testcase+1]["err"] = ["Empty output"]

        elif len(tmp_err_list) > 0 or len(output) != len(answer):
            result_dict[student_id][index_problem][testcase+1]["pass"] = False
            result_dict[student_id][index_problem][testcase+1]["err"] = tmp_err_list
 


def parse_json_to_csv():
    """Convert the grading results from JSON to CSV."""
    with open('result/result.json', 'r') as json_file:
        result_dict = json.load(json_file)

    num_problems = len(os.listdir('./template'))

    with open('result/result.csv', 'w') as f:

        f.write("Student ID, Late Submission")
        for index_problem in range(1, num_problems+1):
            f.write(f",{index_problem}")
        f.write(",Score\n")

        for student_id, problem in result_dict.items():
            score = calculate_score(problem, num_problems)
            write_student_results(f, student_id, problem, score)


def calculate_score(problem, num_problems):
    """Calculate the final score for a student."""
    score = 0
    num_problems = len(os.listdir('./template'))

    for i in range(1, num_problems+1):
        i = str(i)
        if i not in problem:
            continue

        if 'err' in problem[i]:
            continue

        num_pass = sum(1 for _, result in problem[i].items() if result['pass'])
        num_testcase = len(problem[i])
        score += (num_pass/float(num_testcase)) * (100/num_problems)

    if problem['late']:
        score *= LATE_PENALTY

    return round(score, 2)


def write_student_results(f, student_id, problem, score):
    """Write the grading results for a student to the CSV file."""
    f.write(student_id)

    if problem['late']:
        f.write(",Yes")
    else:
        f.write(",No")

    num_problems = len(os.listdir('./template'))

    for i in range(1, num_problems+1):
        i = str(i)
        if i not in problem:
            f.write(", ")
            continue

        if 'err' in problem[i]:
            f.write(f", Error")
            continue

        num_pass = sum(1 for _, result in problem[i].items() if result['pass'])
        num_testcase = len(problem[i])

        f.write(f",{num_pass} of {num_testcase}")

    f.write(f",{score}\n")


if __name__ == "__main__":

    print("\n-------- Grading Started ---------\n")

    grader = Grader(SUBMISSION_FOLDER_PATH, LATE_SUBMISSION_FOLDER_PATH)
    result_dict = grader.grading(SUBMISSION_FOLDER_PATH)

    print("\n-------- Grading Late Submission ---------\n")

    result_dict_late = grader.grading(LATE_SUBMISSION_FOLDER_PATH, late=True)

    print("\n-------- Grading Done ---------\n")

    merge_dict = {**result_dict, **result_dict_late}

    with open('result/result.json', 'w') as json_file:
        json.dump(merge_dict, json_file, indent=4 )

    print("\n-------- Parsing JSON to CSV ---------\n")

    parse_json_to_csv()

    print("\n-------- Done ---------\n")
