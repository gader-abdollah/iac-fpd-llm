import yaml
import pandas as pd
import subprocess

MIN_LINES = 5

def get_folder_name(path):
    return path.split('/repos/')[1].split('/')[0]

def get_repo_url_ez(search_term):
    pwd = subprocess.check_output('realpath ../repos/', shell=True).decode('utf-8').strip()
    command = f"cd {pwd}/{search_term} && git remote get-url origin"
    output = subprocess.check_output(command, shell=True)
    return output.decode('utf-8')[:-1]

# Function to fetch code block from file
def get_code_block(file_path, start_line, end_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        start_index = max(0, start_line - 1)  # Adjust start index to ensure it's not negative
        end_index = min(start_index + MIN_LINES, len(lines)) if end_line <= start_line + MIN_LINES else end_line
        return ''.join(lines[start_index:end_index])

# Read the init.yml file
with open('init.yml', 'r') as file:
    data = yaml.safe_load(file)

# Extract vulnerabilities information
vulnerabilities = data.get('vulnerabilities', [])

# Initialize lists to store extracted information
descriptions = []
flags_types = []
identifiers_urls = []
locations_files = []
locations_start_lines = []
locations_end_lines = []
severities = []
repoURLs = []
code_blocks = []

# Extract information from each vulnerability
for vuln in vulnerabilities:
    location = vuln.get('location', {})
    pwd = subprocess.check_output('realpath ../repos/', shell=True).decode('utf-8').strip()
    file_path = pwd + '/' + location.get('file', '')
    folder_name = get_folder_name(file_path)

    descriptions.append(vuln.get('description', ''))
    
    flags = vuln.get('flags', [])
    flags_type = flags[0].get('type', '') if flags else ''  # Extract the type from the first flag if available
    flags_types.append(flags_type)
    
    identifiers = vuln.get('identifiers', [])
    identifiers_url = identifiers[0].get('url', '') if identifiers else ''  # Extract the URL from the first identifier if available
    identifiers_urls.append(identifiers_url)
    
    locations_files.append(file_path)
    locations_start_lines.append(location.get('start_line', ''))
    locations_end_lines.append(location.get('end_line', ''))
    
    severities.append(vuln.get('severity', ''))
    repoURLs.append(get_repo_url_ez(folder_name))

    # Fetch code block
    start_line = location.get('start_line', 0)
    end_line = location.get('end_line', 0)
    code_block = get_code_block(file_path, start_line, end_line)
    code_blocks.append(code_block)

# Create a DataFrame from the extracted information
df = pd.DataFrame({
    'problem': descriptions,
    'severity': severities,
    'flags_type': flags_types,
    'documentation': identifiers_urls,
    'repoURL': repoURLs,
    'file_path': locations_files,
    'start_line': locations_start_lines,
    'end_line': locations_end_lines,
    'code_block': code_blocks
})

df = df.drop_duplicates(subset=['file_path', 'start_line', 'end_line'], keep='first')

# Write the DataFrame to a new CSV file
df.to_csv('data.csv', index=False)
