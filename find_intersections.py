import pandas as pd

# List of CSV files
files = ['snyk/data.csv', 'checkov/data.csv', 'kics/data.csv', 'semgrep/data.csv', 'tfsec/data.csv']

# Dictionary to store dataframes
dfs = {}

# Reading each CSV file into a dataframe and storing in the dictionary
for file in files:
    tool_name = file.split('/')[0]
    df = pd.read_csv(file, usecols=['file_path', 'start_line', 'end_line'])
    df['tool'] = tool_name
    dfs[tool_name] = df

# Merging dataframes
merged_df = pd.concat(dfs.values())

# Pivot table to create columns for each tool
pivot_df = merged_df.pivot_table(index=['file_path', 'start_line', 'end_line'], columns='tool', aggfunc=lambda x: 'X')

# Filling NaN values with empty strings
pivot_df = pivot_df.fillna('')

# Resetting index to flatten the dataframe
intersect_df = pivot_df.reset_index()

# Merge intersecting rows into a single line
intersect_df = intersect_df.groupby(['file_path', 'start_line', 'end_line']).agg(lambda x: ''.join(set(x))).reset_index()

# Function to merge intersecting rows
def merge_intersecting_rows(group):
    merged_rows = []
    group = group.sort_values(by=['start_line'])  # Sort by start_line to ensure proper merging
    
    # Initialize variables for the first row
    start_line = group.iloc[0]['start_line']
    end_line = group.iloc[0]['end_line']
    x_entries = {column: False for column in group.columns if column not in ['file_path', 'start_line', 'end_line']}
    
    # Iterate over rows in the group
    for _, row in group.iterrows():
        if row['start_line'] <= end_line:  # Check for intersection
            # Update end_line if needed
            end_line = max(end_line, row['end_line'])
            
            # Check for 'X' entries in each column
            for column in x_entries:
                if row[column] == 'X':
                    x_entries[column] = True
        else:
            # Append the merged row to the result
            merged_row = row.copy()
            merged_row['start_line'] = start_line
            merged_row['end_line'] = end_line
            # Update 'X' entries in the merged row
            for column, has_x in x_entries.items():
                if has_x:
                    merged_row[column] = 'X'
            merged_rows.append(merged_row)
            # Update start_line and end_line for the next range
            start_line = row['start_line']
            end_line = row['end_line']
            x_entries = {column: False for column in group.columns if column not in ['file_path', 'start_line', 'end_line']}
    
    # Append the last merged row
    merged_row = group.iloc[-1].copy()
    merged_row['start_line'] = start_line
    merged_row['end_line'] = end_line
    for column, has_x in x_entries.items():
        if has_x:
            merged_row[column] = 'X'
    merged_rows.append(merged_row)
    
    return pd.DataFrame(merged_rows)

# Group by file path and apply merge_intersecting_rows function
merged_df = intersect_df.groupby('file_path').apply(merge_intersecting_rows).reset_index(drop=True)

# Counting number of entries in the 'snyk' column
snyk_count = merged_df['snyk'].value_counts().get('X', 0)
checkov_count = merged_df['checkov'].value_counts().get('X', 0)
kics_count = merged_df['kics'].value_counts().get('X', 0)
semgrep_count = merged_df['semgrep'].value_counts().get('X', 0)
tfsec_count = merged_df['tfsec'].value_counts().get('X', 0)

print("Number of vulnerabilities in 'snyk':", snyk_count)
print("Number of vulnerabilities in 'checkov':", checkov_count)
print("Number of vulnerabilities in 'kics':", kics_count)
print("Number of vulnerabilities in 'semgrep':", semgrep_count)
print("Number of vulnerabilities in 'tfsec':", tfsec_count)

# Save to a new CSV file
merged_df.to_csv('intersections.csv', index=False)
