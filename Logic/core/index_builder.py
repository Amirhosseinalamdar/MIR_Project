from preprocess import Preprocessor
import json
from indexer.indexes_enum import Indexes
from indexer.index import Index
from indexer.tiered_index import Tiered_index
from indexer.metadata_index import Metadata_index
from indexer.document_lengths_index import DocumentLengthsIndex


class Builder():
    def __init__(self, crawled_path = "../Logic/IMDB_crawled.json", data_amount = 100):
        self.path = crawled_path
        self.data_amount = data_amount
        objects = self.read_json()
        
        path = '../Logic/core/indexer/index/'
        self.index = Index(objects)
        self.index.store_index(path+'raw_'+Indexes.DOCUMENTS.value+'_index.json', Indexes.DOCUMENTS.value)

        self.preprocess_objects(objects, Indexes.SUMMARIES.value)
        self.preprocess_objects(objects, Indexes.STARS.value)
        self.preprocess_objects(objects, Indexes.GENRES.value)
        

        self.index = Index(objects)

        self.index.store_index(path+Indexes.SUMMARIES.value+'_index.json', Indexes.SUMMARIES.value)
        self.index.store_index(path+Indexes.DOCUMENTS.value+'_index.json', Indexes.DOCUMENTS.value)
        self.index.store_index(path+Indexes.GENRES.value+'_index.json', Indexes.GENRES.value)
        self.index.store_index(path+Indexes.STARS.value+'_index.json', Indexes.STARS.value)

        Tiered_index(path=path)
        DocumentLengthsIndex(path)
        Metadata_index(path).store_metadata_index(path)


    def read_json(self):
        with open(self.path, "r") as f:
            all_objects = json.load(f)
            objects = all_objects[:self.data_amount]
        return objects

    def preprocess_objects(self, objects: list, type: str):
        for obj in objects:
            obj[type] = Preprocessor(obj[type]).preprocess()

    


Builder()


