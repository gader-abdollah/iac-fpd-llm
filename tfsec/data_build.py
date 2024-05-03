import pandas as pd
import os
import subprocess

def convert_to_absolute_path(relative_path):
    base_directory = subprocess.check_output('realpath ../repos/', shell=True).decode('utf-8').strip()
    return os.path.abspath(os.path.join(base_directory, relative_path))

def get_repo_url_ez(search_term):
    search_term = search_term.split('/')[0]
    pwd = subprocess.check_output('realpath ../repos/', shell=True).decode('utf-8').strip()
    command = f"cd {pwd}/{search_term} && git remote get-url origin"
    output = subprocess.check_output(command, shell=True)
    return output.decode('utf-8')[:-1]

def read_code_block(row):
    start_line = row['start_line']
    end_line = row['end_line']
    file_path = row['file_path']
    
    code_lines = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for i in range(start_line - 1, min(end_line, start_line + 5)):
                code_lines.append(lines[i])
        
        return ''.join(code_lines)
    except:
        print(f"Error reading file: {file_path}")
        return "File not found"

df = pd.read_csv('init.csv')

# Rename columns
df.rename(columns={'file': 'file_path', 'line_start': 'start_line', 'line_end': 'end_line','description':'problem','link':'documentation'}, inplace=True)

# Filter out rows containing "github.com" in the file_path column
df = df[~df['file_path'].str.contains("github.com")]

df.insert(3, 'repoURL', df['file_path'].apply(get_repo_url_ez))
df['file_path'] = df['file_path'].apply(convert_to_absolute_path)
df.insert(3, 'code_block', df.apply(read_code_block, axis=1))

df=df.drop_duplicates(subset=['file_path', 'start_line', 'end_line'], keep='first')

# Save the DataFrame to a new CSV file
df.to_csv('data.csv', index=False)
