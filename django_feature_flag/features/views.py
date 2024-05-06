from django.shortcuts import render
from .models import FeatureFlag
import requests
import yaml
import json
import os

def index(request):
    # Retrieve all feature flags from the database
    feature_flags = FeatureFlag.objects.all()
    return render(request, 'index.html', {'feature_flags': feature_flags})

# def my_view(request):
#     # Check feature flag status using Harness API
#     flag_name = 'python_django'
#     api_key = '317dae07-c649-49ee-a726-5c1d5020af54'  # Your Harness API key
#     api_url = f'https://app.harness.io/gateway/api/flag/{flag_name}'
#     headers = {'X-Api-Key': api_key}
    
#     response = requests.get(api_url, headers=headers)
#     print(response.content)
    
#     if response.status_code == 200:
#         # If request is successful, parse JSON response
#         flag_state = response.json().get('environments')[0].get('state')
#         # Check if the flag is enabled or disabled based on the state
#         flag_status_api = flag_state == 'on'
#     else:
#         # If request fails, set flag status to False
#         flag_status_api = False
    
#     # Pass the flag status to the template
#     return render(request, 'my_view.html', {'flag_status': flag_status_api})

# def my_view(request):
#     # Path to the pipeline.yaml file
#     file_path = 'django_flag/pipeline.yaml'
    
#     try:
#         # Read the contents of the file
#         with open(file_path, 'r') as file:
#             yaml_data = yaml.safe_load(file)
        
#         # Extract the flag status from the parsed YAML data
#         flag_status = yaml_data.get('featureFlags', {}).get('flags', [])[0].get('environments', [])[0].get('state')
        
#         # Determine if the flag is enabled or disabled
#         if flag_status == 'on':
#             flag_status_text = 'enabled'
#         else:
#             flag_status_text = 'disabled'
#     except FileNotFoundError:
#         # Handle the case where the file does not exist
#         flag_status_text = 'file not found'
    
#     # Pass the flag status to the template
#     return render(request, 'my_view.html', {'flag_status': flag_status_text})

def my_view(request):
    # Define the YAML file path
    yaml_file_path = '/Users/akumarjha/project/pythondjango_featureflag/pipeline.yaml'

    # Load the YAML data from the file
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    # Convert YAML data to JSON
    json_data = json.dumps(yaml_data)

    # Load JSON data
    data = json.loads(json_data)

    # Initialize flag status as False by default
    flag_status = False

    # Check if the expected keys are present
    if 'featureFlags' in data and 'flags' in data['featureFlags']:
        # Iterate through the flags to find the state value that is 'on'
        for flag_data in data['featureFlags']['flags']:
            if flag_data['flag']['name'] == 'python_djnago':
                if 'environments' in flag_data['flag']:
                    for environment in flag_data['flag']['environments']:
                        if environment.get('state') == 'on':
                            flag_status = True
                            break  # Break the loop once the flag state is found
                else:
                    print("No environments found for this flag")
                    break
    else:
        print("JSON data structure is not as expected.")

    print("Flag Status (Final):", flag_status)  # Print the final flag status

    # Render the template with the feature flag status
    return render(request, 'my_view.html', {'flag_status': flag_status})