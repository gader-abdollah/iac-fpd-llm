import requests
import os

PER_PAGE = 100
GITHUB_TOKEN = 'YOUR_TOKEN'
TOTAL_REPOS = 151

def search_and_clone_terraform_repos(query, token, output_dir, total_repos=100):
    headers = {'Authorization': f'token {token}'}
    search_url = 'https://api.github.com/search/repositories'
    repos = []
    page = 1

    while len(repos) < total_repos:
        params = {'q': query, 'per_page': PER_PAGE, 'page': page}
        
        response = requests.get(search_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Failed to search repositories. Status code: {response.status_code}")
            return
        
        repos.extend(response.json()['items'])
        print(f"Page {page}: Found {len(response.json()['items'])} repositories")
        
        if len(response.json()['items']) < PER_PAGE:
            break  # No more repositories to fetch
        
        page += 1
    
    print(f"Total repositories fetched: {len(repos)}")
    
    # Clone repositories
    for repo in repos[:total_repos]:
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
search_and_clone_terraform_repos(query, token, output_dir, total_repos=TOTAL_REPOS)
