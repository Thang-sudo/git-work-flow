import sys;
import yaml;
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
    result = subprocess.run(command, capture_output=True, text=True)

    if result.check_returncode == 0:
        return result.stdout.strip()
    else:
        print("ERROR: Failed to execture git rev-parse command")
        return None

def get_changed_files(commit_sha):
    if commit_sha is None:
        print("ERROR: the commit_sha is None")
        return []
    # Run get diff-tree command to get list of changed files
    command = ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_sha]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        changed_files = result.stdout.strip().split('\n')
        return changed_files
    else:
        print("ERROR: Failed to get list of changed yaml files")
        return []

if __name__ == "__main__":
    commit_sha = get_current_commit_sha()
    changed_files = get_changed_files(commit_sha)
    print("list of changed files: ")
    for file in changed_files:
        print(file)

