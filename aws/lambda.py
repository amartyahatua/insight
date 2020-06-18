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
    objectList = payload[0]
    test_data_new = np.zeros((1, 500))
    result = []
    
    for i in range(len(objectList)):
        temp = objectList[i]
        temp = temp.split(" ")
            #print(temp)
        for j in range(len(temp)):
            x = temp[j]
            if(len(x) > 0):
                x = x.lower()
                print(x)
                p = myList[x]
                #print(p)

                test_data_new[0][(j*100):((j+1)*100)] = p
                
        response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,Body=json.dumps([test_data_new]))
        
        result.append(self.knn.predict(test_data_new))
    print("Class --> ",result[0])
    
    
    print(r)
    print(myList[payload[0][0]])
    print("=============yes==@@@@@@@@@@=============")