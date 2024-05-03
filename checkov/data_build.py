import pandas as pd
import json
import subprocess

# Read the json file
with open('init.json', 'r') as file:
    json_data = json.load(file)

def get_folder_name(path):
    return path.split('/repos/')[1].split('/')[0]

def get_repo_url_ez(search_term):
    pwd = subprocess.check_output('realpath ../repos/', shell=True).decode('utf-8').strip()
    command = f"cd {pwd}/{search_term} && git remote get-url origin"
    output = subprocess.check_output(command, shell=True)
    return output.decode('utf-8')[:-1]

# Extracting necessary data from the JSON
data = []
for item in json_data:
    for failed_check in item['results']['failed_checks']:
        pwd = subprocess.check_output('realpath ../repos/', shell=True).decode('utf-8').strip()
        target_file_path = f"{pwd}" + failed_check['file_path']
        row = {}
        row['framework'] = item['check_type']
        row['check_id'] = failed_check['check_id']
        row['documentation'] = failed_check['guideline']
        row['problem'] = failed_check['check_name']
        row['repoURL'] = get_repo_url_ez(get_folder_name(target_file_path))
        row['file_path'] = target_file_path
        row['start_line'] = failed_check['file_line_range'][0]
        row['end_line'] = failed_check['file_line_range'][1]
        
        # Filter out empty lines from code block using strip()
        code_lines = [line[1].strip('\n') for line in failed_check['code_block']]
        if not all(line == '' for line in code_lines):
            row['code_block'] = '\n'.join(code_lines)
            data.append(row)

# Converting to DataFrame
df = pd.DataFrame(data)

# Drop duplicates
df = df.drop_duplicates(subset=['file_path', 'start_line', 'end_line'], keep='first')

# Writing to CSV
df.to_csv('data.csv', index=False)
