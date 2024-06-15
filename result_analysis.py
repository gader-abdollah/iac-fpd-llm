import pandas as pd

# Load the CSV file
file_path = 'vulnerability_analysis.csv'
df = pd.read_csv(file_path)

# Calculate the total number of entries
total_entries = len(df)

# Calculate the number of true positives and false positives
true_positives = len(df[df['vulnerable?'] == 'yes'])
false_positives = len(df[df['vulnerable?'] == 'no'])

# Calculate the percentages
percent_true_positives = (true_positives / total_entries) * 100
percent_false_positives = (false_positives / total_entries) * 100

# Print the results
print(f"Total entries: {total_entries}")
print(f"True positives: {true_positives} ({percent_true_positives:.2f}%)")
print(f"False positives: {false_positives} ({percent_false_positives:.2f}%)")
