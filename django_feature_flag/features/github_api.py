import requests
import yaml

def get_pipeline_yaml():
    # GitHub repository information
    owner = 'jha713'
    repo = 'django_flag'
    file_path = 'https://github.com/jha713/djnago_flag/blob/main/pipeline.yaml'
    branch = 'main'  # or specify the branch name

    # GitHub API endpoint for raw file contents
    api_url = f'https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}'

    # Make HTTP GET request to fetch file contents
    response = requests.get(api_url)

    # Check if request was successful
    if response.status_code == 200:
        # Parse YAML data from response content
        yaml_data = yaml.safe_load(response.content)
        return yaml_data
    else:
        # Handle error (e.g., file not found)
        return None

# Example usage
pipeline_yaml = get_pipeline_yaml()
if pipeline_yaml:
    print(pipeline_yaml)
