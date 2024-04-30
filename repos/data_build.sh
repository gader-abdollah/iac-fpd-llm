#!/bin/bash

snyk iac test --json > ../snyk/init.json
echo "Snyk done"
checkov -d . -o json --output-file-path ../checkov/; mv ../checkov/results_json.json ../checkov/init.json
echo "Checkov done"
docker run --rm -v $(pwd):/path checkmarx/kics:latest scan -p "/path" --report-formats csv -o "/path/"; mv results.csv ../kics/init.csv
echo "Kics done"
semgrep scan --config=auto --gitlab-sast -o $(pwd)/../semgrep/init.yml
echo "Semgrep done"
tfsec . --format csv -O ../tfsec/init.csv
echo "tfsec done"