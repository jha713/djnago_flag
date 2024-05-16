from django.shortcuts import render
from .models import FeatureFlag
import requests
import yaml
import json
import os
import asyncio
import aiofiles

# def index(request):
#     # Retrieve all feature flags from the database
#     feature_flags = FeatureFlag.objects.all()
#     return render(request, 'index.html', {'feature_flags': feature_flags})

# def my_view(request):
#     # Define the YAML file path
#     yaml_file_path = '/Users/akumarjha/project/pythondjango_featureflag/pipeline.yaml'

#     # Load the YAML data from the file
#     with open(yaml_file_path, 'r') as file:
#         yaml_data = yaml.safe_load(file)

#     # Convert YAML data to JSON
#     json_data = json.dumps(yaml_data)

#     # Load JSON data
#     data = json.loads(json_data)

#     # Initialize flag status as False by default
#     flag_status = False

#     # Check if the expected keys are present
#     if 'featureFlags' in data and 'flags' in data['featureFlags']:
#         # Iterate through the flags to find the state value that is 'on'
#         for flag_data in data['featureFlags']['flags']:
#             if flag_data['flag']['name'] == 'python_djnago':
#                 if 'environments' in flag_data['flag']:
#                     for environment in flag_data['flag']['environments']:
#                         if environment.get('state') == 'on':
#                             flag_status = True
#                             break  # Break the loop once the flag state is found
#                 else:
#                     print("No environments found for this flag")
#                     break
#     else:
#         print("JSON data structure is not as expected.")

#     print("Flag Status (Final):", flag_status)  # Print the final flag status

#     # Render the template with the feature flag status
#     return render(request, 'my_view.html', {'flag_status': flag_status})
async def my_view():
    # Define the YAML file path
    yaml_file_path = '/Users/akumarjha/project/pythondjango_featureflag/pipeline.yaml'

    try:
        # Load the YAML data from the file asynchronously
        async with aiofiles.open(yaml_file_path, 'r') as file:
            yaml_data = await file.read()

        # Convert YAML data to JSON
        json_data = yaml.safe_load(yaml_data)

        # Initialize flag status as False by default
        flag_status = False

        # Check if the expected keys are present
        if 'featureFlags' in json_data and 'flags' in json_data['featureFlags']:
            # Iterate through the flags to find the state value that is 'on'
            for flag_data in json_data['featureFlags']['flags']:
                if flag_data['flag']['name'] == 'python_django':
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
        #return render(request, 'my_view.html', {'flag_status': flag_status})
    
    except FileNotFoundError:
        print(f"File not found: {yaml_file_path}")
    except yaml.YAMLError as e:
        print(f"Error while parsing YAML: {e}")

async def main():
    await my_view()

asyncio.run(main())
