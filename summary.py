import pandas as pd

# Read intersect.csv
intersect_df = pd.read_csv('intersections.csv')

# Find file paths that have an 'X' under each of the five specified columns
file_paths = intersect_df[(intersect_df['snyk'] == 'X') &
                          (intersect_df['checkov'] == 'X') &
                          (intersect_df['kics'] == 'X') &
                          (intersect_df['semgrep'] == 'X')]['file_path'].unique()
                        #   (intersect_df['tfsec'] == 'X')]['file_path'].unique()

# Create summary DataFrame
summary_df = pd.DataFrame({'file_path': file_paths})
print(f"Total number of intersections: {summary_df['file_path'].count()}")

# Save to summary.csv
summary_df.to_csv('summary.csv', index=False)
