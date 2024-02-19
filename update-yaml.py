import sys;
import yaml;
import os;
import subprocess;
from datetime import datetime;

def calculate_age(dob):
    today = datetime.today()
    dob_date = datetime.strptime(dob, '%Y-%m-%d')
    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    return age

def update_yaml_file(input_file, output_file):
    with open(input_file, 'r') as f:
        data = yaml.safe_load(f)
    for entry in data:
        dob = entry.get('dob')
        if dob:
            age = calculate_age(dob)
            entry['age'] = age
            del entry['dob']
    
    with open(output_file, 'w') as f:
        yaml.dump(data, f)

def get_current_commit_sha():
    command = ["git", "rev-parse", "HEAD"]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print("Currnet commit sha: " + result.stdout)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("ERROR: Failed to get commit sha " + e)
        return None
    
    # if result.check_returncode == 0:
    #     return result.stdout.strip()
    # else:
    #     print("ERROR: Failed to execture git rev-parse command" + result.stderr)
    #     return None

def get_changed_files(commit_sha):
    if commit_sha is None:
        print("ERROR: the commit_sha is None")
        return []
    # Run get diff-tree command to get list of changed files
    command = ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_sha]
    try:
        changed_files = subprocess.check_output(command).decode('utf-8').strip().split('\n')
        print("get_changed_files returns: " + changed_files)
        return changed_files
    except subprocess.CalledProcessError as e:
        print("ERROR: Failed to get list of changed files " + e)
        return []

if __name__ == "__main__":
    commit_sha = get_current_commit_sha()
    changed_files = get_changed_files(commit_sha)
    print("list of changed files: ")
    for file in changed_files:
        print(file)

