# views.py
from django.shortcuts import render
from .models import FeatureFlag , Employee
import requests
import yaml
import json
import os
import asyncio
import aiofiles
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .ymlscripts import get_flag_status
from .serializers import EmployeeSerializer
from rest_framework import status

@api_view(['GET'])
def flag_status_api(request):
    flag_status = get_flag_status()
    print("Flag Status:", flag_status)  # Print flag status in the terminal
    return Response({'flag_status': flag_status})

@api_view(['GET', 'POST'])
def employees(request):
    flag_status = get_flag_status()

    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if flag_status:
            serializer = EmployeeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You are not allowed to create new employees because the feature flag is off."}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({"message": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    flag_status = get_flag_status()

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if flag_status:
            serializer = EmployeeSerializer(employee, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You are not allowed to update employees because the feature flag is off."}, status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'DELETE':
        if flag_status:
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You are not allowed to delete employees because the feature flag is off."}, status=status.HTTP_403_FORBIDDEN)
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
