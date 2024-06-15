import pandas as pd
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def check_vulnerability(code_block):
    prompt = f"""
    Here is a block of code:

    {code_block}

    Please analyze the code and answer the following questions:
    1. Is there a security vulnerability in this code? Answer 'yes' or 'no'.
    2. If no, explain why, considering that 4 SAST tools have agreed on the vulnerability.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes code for security vulnerabilities."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response['choices'][0]['message']['content'].strip()

# Read the summary.csv file
summary_df = pd.read_csv('summary.csv')

# Create lists to store results
vulnerable = []
causes = []

# Process each code block
for _, row in summary_df.iterrows():
    result = check_vulnerability(row['code_block'])

    # Initialize variables
    vulnerability_answer = "no"
    cause = ""

    # Parse the result
    lines = result.split('\n')

    # Collect answers from the response
    for line in lines:
        if line.startswith("1."):
            if "yes" in line.lower():
                vulnerability_answer = "yes"
            elif "no" in line.lower():
                vulnerability_answer = "no"
        elif line.startswith("2."):
            cause = line.split("2.")[1].strip()

    # Append results to the lists
    vulnerable.append(vulnerability_answer)
    causes.append(cause)

# Add results to the DataFrame
summary_df['vulnerable?'] = vulnerable
summary_df['cause'] = causes

# Save the results to a new CSV file
summary_df.to_csv('vulnerability_analysis.csv', index=False)

print("Vulnerability analysis completed and saved to vulnerability_analysis.csv")
