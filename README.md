# iac-fpd-llm
IaC script vulnerability false positive detection using open source LLM(s)

## Set important variables

repos/repo_build.py:
* __PER_PAGE__: Number of repos in a single query (100, can be left unchanged)
* __GITHUB_TOKEN__: Your personal token used to make queries using the github api (will not work without it)
* __TOTAL_REPOS__: Number of repos to clone (Adapt accordingly)

## Important points

* The installation guide is geared towards Ubuntu machines. You have to adapt the installation scripts to your own OS.
* The intersection and summary scripts will only work if each tool returns at least 1 entry
* By default, tfsec is ignored in the summary script because it severely limits the number of intersections

## Necessary dependencies
* [snyk](https://docs.snyk.io/snyk-cli/install-or-update-the-snyk-cli)
* [checkov](https://www.checkov.io/2.Basics/Installing%20Checkov.html)
* [kics](https://docs.kics.io/1.4.5/getting-started/)
* [semgrep](https://semgrep.dev/docs/getting-started/quickstart)
* [tfsec](https://aquasecurity.github.io/tfsec/v0.63.1/getting-started/installation/)

To install them, you need docker engine, pip, npm and brew
```bash
curl -fsSL https://get.docker.com | sudo sh
sudo apt install pip npm
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## How to install the dependencies
```bash
sudo npm install snyk -g
pip install checkov
sudo docker pull checkmarx/kics:latest
python3 -m pip install semgrep
brew install tfsec
```

## Initial setup
This is required in order for the tools to function as expected.
The snyk API key can be found in the account profile as of May 2024.
```bash
snyk auth <API_KEY>
semgrep login
```

## How to run the experiment
You can copy and paste this script in the terminal once you are in the 
project's root directory.  
NOTE: If your system does not have 'python3', try 'python'.
```bash
cd repos
python3 repo_build.py
snyk iac test --json > ../snyk/init.json
checkov -d . -o json --output-file-path ../checkov/; mv ../checkov/results_json.json ../checkov/init.json
sudo docker run --rm -v $(pwd):/path checkmarx/kics:latest scan -p "/path" --timeout 600 --report-formats csv -o "/path"; mv results.csv ../kics/init.csv
semgrep scan --config=auto --no-git-ignore --max-target-bytes=0 --timeout=0 --gitlab-sast -o $(pwd)/../semgrep/init.yml
tfsec . --ignore-hcl-errors --format csv -O ../tfsec/init.csv
cd ../snyk
python3 data_build.py
cd ../checkov
python3 data_build.py
cd ../kics
python3 data_build.py
cd ../semgrep
python3 data_build.py
cd ../tfsec
python3 data_build.py
cd ..
python3 find_intersections.py
python3 summary.py
```
