# ymlscripts.py
import asyncio
import aiofiles
import yaml

async def my_view():
    yaml_file_path = '/Users/akumarjha/project/pythondjango_featureflag/pipeline.yaml'
    try:
        async with aiofiles.open(yaml_file_path, 'r') as file:
            yaml_data = await file.read()
        json_data = yaml.safe_load(yaml_data)
        flag_status = False
        if 'featureFlags' in json_data and 'flags' in json_data['featureFlags']:
            for flag_data in json_data['featureFlags']['flags']:
                if flag_data['flag']['name'] == 'python_djnago':
                    if 'environments' in flag_data['flag']:
                        for environment in flag_data['flag']['environments']:
                            if environment.get('state') == 'on':
                                flag_status = True
                                break
                    else:
                        print("No environments found for this flag")
                        break
        else:
            print("JSON data structure is not as expected.")
        return flag_status
    
    except FileNotFoundError:
        print(f"File not found: {yaml_file_path}")
    except yaml.YAMLError as e:
        print(f"Error while parsing YAML: {e}")
    while True:
        await asyncio.sleep(1)

def get_flag_status():
    return asyncio.run(my_view())

if __name__ == '__main__':
    flag_status = get_flag_status()
    print(f"Flag status: {flag_status}")
