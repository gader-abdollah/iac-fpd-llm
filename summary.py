import pandas as pd

# Read intersect.csv
intersect_df = pd.read_csv('intersections.csv')

# Find file paths that have an 'X' under each of the specified columns
filtered_df = intersect_df[(intersect_df['snyk'] == 'X') &
                           (intersect_df['checkov'] == 'X') &
                           (intersect_df['kics'] == 'X') &
                           (intersect_df['semgrep'] == 'X')]
                           # (intersect_df['tfsec'] == 'X')]

# Create summary DataFrame with file_path, start_line, and end_line columns
summary_df = filtered_df[['file_path', 'start_line', 'end_line']].drop_duplicates()

# Define a function to read code blocks from file
def get_code_block(file_path, start_line, end_line):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            start_index = max(0, start_line - 1)
            end_index = max(start_index + 4, end_line)
            return ''.join(lines[start_index:end_index])
    except Exception as e:
        return f"Error reading file: {e}"

# Apply the function to each row to create the code_block column
summary_df['code_block'] = summary_df.apply(
    lambda row: get_code_block(row['file_path'], row['start_line'], row['end_line']),
    axis=1
)

# Print the total number of intersections
print(f"Total number of intersections: {summary_df.shape[0]}")

# Save to summary.csv
summary_df.to_csv('summary.csv', index=False)
