from  similarity import Similarity
from objectdetection import ObjectDetction

class GarbageClassification:
    def find(self):
        print("Finding similarity")
        simi = Similarity()
        embeddings_index, knn = simi.similarity()
        print("***************")
        #obj = ObjectDetction()
        #obj.identify(embeddings_index, knn)
        
garbage = GarbageClassification()
garbage.find()
        
        