import os
import io
import boto3
import json
import pickle
import numpy

# grab environment variables



bucket = 'sagemaker-us-east-2-359780414608'
key = 'myfile.pkl'

s3 = boto3.client('s3')
object = s3.get_object(Bucket=bucket, Key=key)

body_string = object['Body'].read()
myList = pickle.loads(body_string)
r = len(myList)

ENDPOINT_NAME = 'sagemaker-scikit-learn-2020-06-16-04-19-43-119'
runtime= boto3.client('runtime.sagemaker')





def lambda_handler(event, context):

    data = json.loads(json.dumps(event))
    payload = data['data']
    print(payload)
    objectList = payload[0]
    print(objectList)
    result = []
    
    p = myList[objectList[0]]
    p = p.tolist()
    for i in range(400):
        p.append(0)

    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME, Body=json.dumps([p]))
    result = json.loads(response['Body'].read().decode())
    
    return result[0]