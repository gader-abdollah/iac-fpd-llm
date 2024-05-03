import pandas as pd
import subprocess

def get_folder_name(path):
    return path.split('/repos/')[1].split('/')[0]

def get_repo_url_ez(search_term):
    pwd = subprocess.check_output('realpath ../repos/', shell=True).decode('utf-8').strip()
    command = f"cd {pwd}/{search_term} && git remote get-url origin"
    output = subprocess.check_output(command, shell=True)
    return output.decode('utf-8')[:-1]

def get_line_content_more(file_path, start_line):
    try:
        start_line = max(start_line, 1)  # Ensure start_line is not negative
        with open(file_path, 'r') as file:
            file_lines = file.readlines()
            if len(file_lines) < start_line:
                raise ValueError("Start line is out of range")
            open_braces_count = file_lines[start_line - 1].count("{")
            output_line = file_lines[start_line - 1]
            end_line = start_line

            if open_braces_count == 0:
                line_difference = 5
                for line_index in range(start_line, len(file_lines)):
                    output_line += file_lines[line_index]
                    end_line = line_index + 1
                    if line_index - start_line == line_difference:
                        break
                return output_line, end_line

            for line in file_lines[start_line:]:
                end_line += 1
                if open_braces_count != 0:
                    if line.strip() != '':
                        output_line += line
                    open_braces_count += line.count("{")
                    open_braces_count -= line.count("}")
                    if open_braces_count == 0:
                        break
        return output_line, end_line
    except Exception as e:
        print(f"Error processing file: {file_path}, start_line: {start_line}, Error: {e}")
        return "", start_line

# Read the original CSV file
df = pd.read_csv('init.csv')

# Replace the specified substring in the file_name column
pwd = subprocess.check_output('realpath ../repos/', shell=True).decode('utf-8').strip()
df['file_path'] = df['file_name'].str.replace('../../path',pwd)

# Drop the specified columns and rename the rest
df = df[['file_path', 'line', 'query_uri', 'description']]
df.columns = ['file_path', 'start_line', 'documentation', 'problem']

# Add a new column called 'code_block' after 'start_line'
df['code_block'], df['end_line'] = zip(*df.apply(lambda row: get_line_content_more(row['file_path'], row['start_line']), axis=1))

# Get repository URLs for each folder
df['repoURL'] = df['file_path'].apply(lambda path: get_repo_url_ez(get_folder_name(path)))

# Rearrange columns
df = df[['file_path', 'start_line', 'end_line', 'code_block', 'repoURL', 'documentation', 'problem']]

# Drop duplicates based on file path, start line, and end line
df.drop_duplicates(subset=['file_path', 'start_line', 'end_line'], keep='first', inplace=True)

# Write the modified data to a new CSV file
df.to_csv('data.csv', index=False)
