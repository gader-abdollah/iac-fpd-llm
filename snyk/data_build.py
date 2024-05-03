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
    start_line = 1 if start_line < 0 else start_line
    with open(file_path, 'r') as file:
        file_lines = file.readlines()
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

        # Start from the specified line and continue until the first closing curly brace
        for line in file_lines[start_line:]:
            end_line += 1
            if open_braces_count != 0:
                if line.strip() != '':
                    output_line += line
                open_braces_count += line.count("{")
                open_braces_count -= line.count("}")

                # If the open and close braces are balanced and the first open brace has been closed
                if open_braces_count == 0:
                    break
    return output_line, end_line


# Read the json file and drop unnecessary columns
df = pd.read_json('init.json')
df = df.drop(columns=['vulnerabilities','meta','filesystemPolicy','dependencyCount','licensesPolicy','ignoreSettings','projectName','org','policy','isPrivate','targetFile','packageManager','path'])
cols = ['targetFilePath']
iac_cols = ['id','issue','severity','documentation','lineNumber','impact','resolve']

data = []
for file, target_file_path in zip(df['infrastructureAsCodeIssues'], df['targetFilePath']):
    for vulnerability in file:
        row = {}
        row['id'] = vulnerability['id']
        row['severity'] = vulnerability['severity']
        row['documentation'] = vulnerability['documentation']
        row['problem'] = vulnerability['issue']
        row['impact'] = vulnerability['impact']
        row['resolve'] = vulnerability['resolve']
        row['repoURL'] = get_repo_url_ez(get_folder_name(target_file_path))
        row['file_path'] = target_file_path
        row['start_line'] = vulnerability['lineNumber'] + 1 if vulnerability['lineNumber'] < 0 else vulnerability['lineNumber']
        code_block, end_line = get_line_content_more(target_file_path, vulnerability['lineNumber'])
        row['end_line'] = end_line
        row['code block'] = code_block
        data.append(row)

df_output = pd.DataFrame(data)

# Drop duplicates
df_output = df_output.drop_duplicates(subset=['file_path', 'start_line', 'end_line'], keep='first')

df_output.to_csv('data.csv', index=False)
