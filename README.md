# iac-fpd-llm
IaC script vulnerability false positive detection using open source LLM(s)

## Set important variables

__PER_PAGE__: The number of repositories to clone (5 by default)  
__GITHUB_TOKEN__: Your personal token used to make queries using the github api (will not work without it)

## Important points

* The intersection and summary scripts will only work if each tool returns at least 1 entry
* By default, tfsec is ignored in the summary script because it severely limits the number of intersections

## How to run the experiment
```bash
cd repos
python repo_build.py
snyk iac test --json > ../snyk/init.json
checkov -d . -o json --output-file-path ../checkov/; mv ../checkov/results_json.json ../checkov/init.json
docker run --rm -v $(pwd):/path checkmarx/kics:latest scan -p "/path" --report-formats csv -o "/path"; mv results.csv ../kics/init.csv
semgrep scan --config=auto --gitlab-sast -o $(pwd)/../semgrep/init.yml
tfsec . --format csv -O ../tfsec/init.csv
cd ../snyk
python data_build.py
cd ../checkov
python data_build.py
cd ../kics
python data_build.py
cd ../semgrep
python data_build.py
cd ../tfsec
python data_build.py
cd ..
python find_intersections.py
python summary.py
```
