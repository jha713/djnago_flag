import yaml
import json

# Load the YAML data from the file
with open('/Users/akumarjha/project/pythondjango_featureflag/djnago_flag/pipeline.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

# Convert YAML data to JSON
json_data = json.dumps(yaml_data)

# Load JSON data
data = json.loads(json_data)
print('Pipeline file data:', data)

# Check if the expected keys are present
if 'featureFlags' in data and 'flags' in data['featureFlags']:
    # Iterate through the flags to find the state value that is 'on'
    for flag_data in data['featureFlags']['flags']:
        print("Flag:", flag_data['flag']['name'])
        if 'environments' in flag_data['flag']:
            for environment in flag_data['flag']['environments']:
                print("Environment:", environment['identifier'])
                if environment.get('state') == 'on':
                    state_value = environment['state']
                    print("State value that is currently 'on':", state_value)
                else:
                    print("State value:", environment.get('state', 'N/A'))
        else:
            print("No environments found for this flag")
else:
    print("JSON data structure is not as expected.")
