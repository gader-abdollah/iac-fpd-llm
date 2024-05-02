# iac-fpd-llm
IaC script vulnerability false positive detection using open source LLM(s)

## How to run the experiment
```bash
cd repos
python repo_build.py
snyk iac test --json > ../snyk/init.json
checkov -d . -o json --output-file-path ../checkov/; mv ../checkov/results_json>
docker run --rm -v $(pwd):/path checkmarx/kics:latest scan -p "/path" --report->
semgrep scan --config=auto --gitlab-sast -o $(pwd)/../semgrep/init.yml
tfsec . --format csv -O ../tfsec/init.csv
```
