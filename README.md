# Github-api-sls

## Summary
This Python serverless function uses the PyGithub library and GitHub API to collect data from a list of specified GitHub
repositories. It retrieves and counts the number of contributors and releases in the past year for each repository,
storing this data in a pandas DataFrame.

## Usage
Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Run Python Script

```bash
serverless invoke local -f hello
```
