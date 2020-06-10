import io
from sklearn.neighbors import KNeighborsClassifier
from google.cloud import vision
import os
import numpy as np

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="client_secrets.json"

class ObjectDetction:
    def __init__(self):
        self.img = "mirror.jpg"
        self.client = vision.ImageAnnotatorClient()
        
    def identify(self, embeddings_index, knn):
        with io.open(self.img,'rb') as image_file:
            content = image_file.read()
            
        image = vision.types.Image(content=content)
        
        objects = self.client.object_localization(
        image=image).localized_object_annotations
        objectList = []

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
                    p = embeddings_index[x]
                    #print(p)

                    test_data_new[0][(j*100):((j+1)*100)] = p
                    result = knn.predict(test_data_new)
                    print("Class --> ",result[0])
