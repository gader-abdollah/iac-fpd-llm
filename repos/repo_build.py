import requests
import os

PER_PAGE = 5
GITHUB_TOKEN = 'YOUR_TOKEN'

def search_and_clone_terraform_repos(query, token, output_dir):
    headers = {'Authorization': f'token {token}'}
    search_url = 'https://api.github.com/search/repositories'
    params = {'q': query, 'per_page': PER_PAGE}  # Limit to 100 items per page
    
    # Search for repositories
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Failed to search repositories. Status code: {response.status_code}")
        return
    
    repos = response.json()['items']
    print(f"Found {len(repos)} repositories")
    
    # Clone repositories
    for repo in repos[:100]:  # Limit to maximum of 100 repositories
        clone_url = repo['clone_url']
        repo_name = repo['name']
        repo_path = os.path.join(output_dir, repo_name)
        
        print(f"Cloning {repo_name}...")
        os.system(f"git clone {clone_url} {repo_path}")
        print(f"Cloned {repo_name} to {repo_path}")

# Set your GitHub personal access token
token = GITHUB_TOKEN

# Set the query to search for Terraform repositories
query = 'language:terraform'

# Set the output directory for cloning repositories
output_dir = '.'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Search for Terraform repositories and clone them
search_and_clone_terraform_repos(query, token, output_dir)