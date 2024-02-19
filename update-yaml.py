import sys;
import yaml;
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

if __name__ == "__main__":
    input_file = sys.argv[1]

