import io
from sklearn.neighbors import KNeighborsClassifier
from google.cloud import vision
import os
import numpy as np
import pickle
import cv2

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="client_secrets.json"

class ObjectDetction:
    def __init__(self, img):
        self.img = img
        self.client = vision.ImageAnnotatorClient()
        self.embeddings_index = pickle.load( open( "embeddings_index.pkl", "rb" ) )
        self.knn = pickle.load(open('finalized_model.sav', 'rb'))
    def identify(self):
        with io.open(self.img,'rb') as image_file:
            content = image_file.read()
            
        image = vision.types.Image(content=content)
        
        objects = self.client.object_localization(
        image=image).localized_object_annotations
        objectList = []
        cls = -1
        print('Number of objects found: {}'.format(len(objects)))
        for object_ in objects:
            print('\n{} (confidence: {})'.format(object_.name, object_.score))
            objectList.append(object_.name)
            print('Normalized bounding polygon vertices: ')
            for vertex in object_.bounding_poly.normalized_vertices:
                print(' - ({}, {})'.format(vertex.x, vertex.y))
                
        test_data_new = np.zeros((1, 500))
        for i in range(len(objectList)):
            temp = objectList[i]
            temp = temp.split(" ")
                #print(temp)
            for j in range(len(temp)):
                x = temp[j]
                if(len(x) > 0):
                    x = x.lower()
                    print(x)
                    p = self.embeddings_index[x]
                    #print(p)

                    test_data_new[0][(j*100):((j+1)*100)] = p
                    result = self.knn.predict(test_data_new)
                    print("Class --> ",result[0])
        
        cls = result[0]
                    
        imgcv = cv2.imread(self.img)
        height = imgcv.shape[0]
        width = imgcv.shape[1]
        
        thickness = 2
        
        for object_ in objects:
            objectname = object_.name
            count = 0
            for vertex in object_.bounding_poly.normalized_vertices:
                if(count == 0):
                    startX = int(width*vertex.x)
                    startY = int(height*vertex.y)
                if(count == 2):
                    endX = int(width*vertex.x)
                    endY = int(height*vertex.y)
                count += 1
                
            if(cls == 0):
                color = (0, 0, 255) 
            elif(cls == 1):
                color = (0, 255, 0) 
            elif(cls == 2):
                color = (255, 0, 0) 
                
            imgcv = cv2.rectangle(imgcv, (startX, startY), (endX, endY), color, thickness) 
            cv2.putText(imgcv, objectname, (startX, (startY-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
        
        cv2.imwrite(self.img, imgcv)
       