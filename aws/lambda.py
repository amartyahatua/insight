import os
import boto3
import pickle
import numpy as np
import json


# grab environment variables
ENDPOINT_NAME = 'sagemaker-scikit-learn-2020-06-16-04-19-43-119'

s3 = boto3.client('s3')
bucket = 'sagemaker-us-east-2-359780414608'
key = 'myfile.pkl'
object = s3.get_object(Bucket=bucket, Key=key)
body_string = object['Body'].read()
myList = pickle.loads(body_string)
r = len(myList)


def lambda_handler(event, context):
    
    data = json.loads(json.dumps(event))
    payload = data['data']
    print(payload)
    
    
    # response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
    #                                   Body=json.dumps(payload))
    # #print(response)
    # result = json.loads(response['Body'].read().decode())
    # #print(result)
    
    # return result[0]
    
    print(r)
    print(myList[payload[0][0]])
    print("=============yes==@@@@@@@@@@=============")