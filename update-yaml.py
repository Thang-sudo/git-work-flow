import sys;
import yaml;
import os;
import subprocess;
from datetime import datetime;
'''
This script will only update age if the yaml file part of commit
'''
def calculate_age(dob):
    today = datetime.today()
    dob_date = datetime.strptime(dob, '%Y-%m-%d')
    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    return age

def update_yaml_file(input_file):
    try:
        with open(input_file, 'r') as f:
            data = yaml.safe_load(f)
        dob = data["dob"]
        if dob:
            age = calculate_age(dob)
            data["age"] = age
        
        with open(input_file, 'w') as f:
            yaml.dump(data, f)
        return input_file
    except FileNotFoundError as e:
        print("File not found: " + input_file)
        return None
    # try:
    #     subprocess.run(["git", "status"])
    #     subprocess.run(["git", "add", input_file])
    #     subprocess.run(["git", "commit", "-m", "Update YAML file " + input_file + " [skip ci]"])
    #     subprocess.run(["git", "push", "origin", "main"])
    #     print("Changes committed to main branch.")
    # except subprocess.CalledProcessError as e:
    #     print("ERROR: Failed to commit changes to main branch:", e)

def get_current_commit_sha():
    command = ["git", "rev-parse", "HEAD"]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print("Currnet commit sha: " + result.stdout)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("ERROR: Failed to get commit sha " + e)
        return None

def get_changed_files(commit_sha):
    if commit_sha is None:
        print("ERROR: the commit_sha is None")
        return []
    # Run get diff-tree command to get list of changed files
    command = ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_sha]
    
    try:
        changed_files = subprocess.check_output(command).decode("utf-8").strip().split('\n')
        return changed_files
    except subprocess.CalledProcessError as e:
        print("ERROR: Failed to get list of changed files " + e)
        return []

if __name__ == "__main__":
    commit_sha = get_current_commit_sha()
    changed_files = get_changed_files(commit_sha)
    updated_files =[]
    print("list of changed yaml files: ")
    for file in changed_files:
        if file.startswith("savedFilters") and (file.endswith(".yaml") or file.endswith(".yml")):
            updated_file = update_yaml_file(file)
            if updated_file is not None:
                updated_files.append(updated_file)
    print('\n'.join(updated_files))
    print("::set-output name=downloaded_files::{}".format(','.join(updated_files)))


