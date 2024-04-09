import time
import os
import json
from enum import Enum
import copy


class Indexes(Enum):
    DOCUMENTS = 'documents'
    STARS = 'stars'
    GENRES = 'genres'
    SUMMARIES = 'summaries'


class Index:
    def __init__(self, preprocessed_documents: list):
        """
        Create a class for indexing.
        """

        self.preprocessed_documents = preprocessed_documents

        self.index = {
            Indexes.DOCUMENTS.value: self.index_documents(),
            Indexes.STARS.value: self.index_stars(),
            Indexes.GENRES.value: self.index_genres(),
            Indexes.SUMMARIES.value: self.index_summaries(),
        }

    def index_documents(self):
        """
        Index the documents based on the document ID. In other words, create a dictionary
        where the key is the document ID and the value is the document.

        Returns
        ----------
        dict
            The index of the documents based on the document ID.
        """

        current_index = {}
        for document in self.preprocessed_documents:
            current_index[document['id']] = copy.deepcopy(document)

        return current_index

    def index_stars(self):
        """
        Index the documents based on the stars.

        Returns
        ----------
        dict
            The index of the documents based on the stars. You should also store each terms' tf in each document.
            So the index type is: {term: {document_id: tf}}
        """
        current = {}
        for doc in self.preprocessed_documents:
            for star in doc[Indexes.STARS.value]:
                for term in star.split():
                    self.add_term_doc_to_index(term, doc, current, Indexes.STARS.value)
        return current
    
    def index_genres(self):
        """
        Index the documents based on the genres.

        Returns
        ----------
        dict
            The index of the documents based on the genres. You should also store each terms' tf in each document.
            So the index type is: {term: {document_id: tf}}
        """

        current = {}
        for doc in self.preprocessed_documents:
            for term in doc[Indexes.GENRES.value]:
                self.add_term_doc_to_index(term, doc, current, Indexes.GENRES.value)           

        return current

    def index_summaries(self):
        """
        Index the documents based on the summaries (not first_page_summary).

        Returns
        ----------
        dict
            The index of the documents based on the summaries. You should also store each terms' tf in each document.
            So the index type is: {term: {document_id: tf}}
        """

        current = {}
        for doc in self.preprocessed_documents:
            for summary in doc[Indexes.SUMMARIES.value]:
                for term in summary.split():
                    self.add_term_doc_to_index(term, doc, current, Indexes.SUMMARIES.value)         

        return current

    def get_posting_list(self, word: str, index_type: str):
        """
        get posting_list of a word

        Parameters
        ----------
        word: str
            word we want to check
        index_type: str
            type of index we want to check (documents, stars, genres, summaries)

        Return
        ----------
        list
            posting list of the word (you should return the list of document IDs that contain the word and ignore the tf)
        """
        try: 
            return list(self.index[index_type][word].keys())                   
        except:
            return []
        
    def add_term_doc_to_index(self, term: str, doc, current: dict, type: str):
        if term not in current:
            current[term] = {}
        if doc['id'] not in current[term]:
            current[term][doc['id']] = 0
        current[term][doc['id']] += 1


    def add_document_to_index(self, document: dict):
        """
        Add a document to all the indexes

        Parameters
        ----------
        document : dict
            Document to add to all the indexes
        """
        if document['id'] not in self.index[Indexes.DOCUMENTS.value]:
            self.index[Indexes.DOCUMENTS.value][document['id']] = copy.deepcopy(document)
            for summary in document[Indexes.SUMMARIES.value]:
                for term in summary.split():
                    self.add_term_doc_to_index(term, document, self.index[Indexes.SUMMARIES.value], Indexes.SUMMARIES.value)

            for star in document[Indexes.STARS.value]:
                for term in star.split():
                    self.add_term_doc_to_index(term, document, self.index[Indexes.STARS.value], Indexes.STARS.value)

            for genre in document[Indexes.GENRES.value]:
                self.add_term_doc_to_index(genre, document, self.index[Indexes.GENRES.value], Indexes.GENRES)

    def remove_document_from_index(self, document_id: str):
        """
        Remove a document from all the indexes

        Parameters
        ----------
        document_id : str
            ID of the document to remove from all the indexes
        """
        if document_id in self.index[Indexes.DOCUMENTS.value]:

            # doc = copy.deepcopy(self.index[Indexes.DOCUMENTS.value][document_id])
            doc = self.index[Indexes.DOCUMENTS.value][document_id]

            for summary in doc[Indexes.SUMMARIES.value]:
                for term in summary.split():
                    del self.index[Indexes.SUMMARIES.value][term][document_id]
                    if not self.index[Indexes.SUMMARIES.value][term]:
                        del self.index[Indexes.SUMMARIES.value][term]                

            for star in doc[Indexes.STARS.value]:
                for term in star.split():
                    del self.index[Indexes.STARS.value][term][document_id]
                    if not self.index[Indexes.STARS.value][term]:
                        del self.index[Indexes.STARS.value][term]


            for term in doc[Indexes.GENRES.value]:
                del self.index[Indexes.GENRES.value][term][document_id]
                if not self.index[Indexes.GENRES.value][term]:
                    del self.index[Indexes.GENRES.value][term]

            del self.index[Indexes.DOCUMENTS.value][document_id]

    def check_add_remove_is_correct(self):
        """
        Check if the add and remove is correct
        """

        dummy_document = {
            'id': '100',
            'stars': ['tim', 'henry'],
            'genres': ['drama', 'crime'],
            'summaries': ['good']
        }

        index_before_add = copy.deepcopy(self.index)
        self.add_document_to_index(dummy_document)
        index_after_add = copy.deepcopy(self.index)

        if index_after_add[Indexes.DOCUMENTS.value]['100'] != dummy_document:
            print('Add is incorrect, document')
            return

        if (set(index_after_add[Indexes.STARS.value]['tim']).difference(set(index_before_add[Indexes.STARS.value].get('tim', {})))
                != {dummy_document['id']}):
            print('Add is incorrect, tim')
            return

        if (set(index_after_add[Indexes.STARS.value]['henry']).difference(set(index_before_add[Indexes.STARS.value].get('henry', {})))
                != {dummy_document['id']}):
            print('Add is incorrect, henry')
            return
        if (set(index_after_add[Indexes.GENRES.value]['drama']).difference(set(index_before_add[Indexes.GENRES.value].get('drama', {})))
                != {dummy_document['id']}):
            print('Add is incorrect, drama')
            return

        if (set(index_after_add[Indexes.GENRES.value]['crime']).difference(set(index_before_add[Indexes.GENRES.value].get('crime', {})))
                != {dummy_document['id']}):
            print('Add is incorrect, crime')
            return

        if (set(index_after_add[Indexes.SUMMARIES.value]['good']).difference(set(index_before_add[Indexes.SUMMARIES.value].get('good', {})))
                != {dummy_document['id']}):
            print('Add is incorrect, good')
            return

        print('Add is correct')

        self.remove_document_from_index('100')
        index_after_remove = copy.deepcopy(self.index)
        
        if index_after_remove == index_before_add:
            print('Remove is correct')
        else:
            print('Remove is incorrect')

    def store_index(self, path: str, index_type: str):
        """
        Stores the index in a file (such as a JSON file)

        Parameters
        ----------
        path : str
            Path to store the file
        index_type: str
            type of index we want to store (documents, stars, genres, summaries)
        """
        

        if index_type not in self.index:
            raise ValueError('Invalid index type')

        try:
            file_path = path
            # file_path = os.path.join(path, f"{index_type}.json")
            with open(file_path, 'w') as file:
                json.dump(self.index[index_type], file)
            
            print(f"Index '{index_type}' stored successfully in '{file_path}'")
        except Exception as e:
            print(f"Error storing index '{index_type}' to file: {e}")


    def load_index(self, path: str):
        """
        Loads the index from a file (such as a JSON file)

        Parameters
        ----------
        path : str
            Path to load the file
        """
        try:
            with open(path, 'r') as file:
                data = file.read()
                index = json.loads(data)
                return index
        except FileNotFoundError:
            print(f"Error: File '{path}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Failed to parse JSON data from file '{path}'.")
            return None
        

    def check_if_index_loaded_correctly(self, index_type: str, loaded_index: dict):
        """
        Check if the index is loaded correctly

        Parameters
        ----------
        index_type : str
            Type of index to check (documents, stars, genres, summaries)
        loaded_index : dict
            The loaded index

        Returns
        ----------
        bool
            True if index is loaded correctly, False otherwise
        """

        return self.index[index_type] == loaded_index

    def check_if_indexing_is_good(self, index_type: str, check_word: str = 'good'):
        """
        Checks if the indexing is good. Do not change this function. You can use this
        function to check if your indexing is correct.

        Parameters
        ----------
        index_type : str
            Type of index to check (documents, stars, genres, summaries)
        check_word : str
            The word to check in the index

        Returns
        ----------
        bool
            True if indexing is good, False otherwise
        """

        # brute force to check check_word in the summaries
        start = time.time()
        docs = []
        for document in self.preprocessed_documents:
            if index_type not in document or document[index_type] is None:
                continue

            for field in document[index_type]:
                if check_word in field:
                    docs.append(document['id'])
                    break

            # if we have found 3 documents with the word, we can break
            if len(docs) == 3:
                break

        end = time.time()
        brute_force_time = end - start

        # check by getting the posting list of the word
        start = time.time()
        # TODO: based on your implementation, you may need to change the following line
        posting_list = self.get_posting_list(check_word, index_type)

        end = time.time()
        implemented_time = end - start

        print('Brute force time: ', brute_force_time)
        print('Implemented time: ', implemented_time)

        if set(docs).issubset(set(posting_list)):
            print('Indexing is correct')

            if implemented_time < brute_force_time:
                print('Indexing is good')
                return True
            else:
                print('Indexing is bad')
                return False
        else:
            print('Indexing is wrong')
            return False



# TODO: Run the class with needed parameters, then run check methods and finally report the results of check methods
file_path = "../../IMDB_crawled.json"

def read_first_100_objects(file_path):
    with open(file_path, "r") as f:
        all_objects = json.load(f)
        first_100_objects = all_objects[:100]
    return first_100_objects

objects = read_first_100_objects(file_path)
index = Index(objects)
# index.check_add_remove_is_correct()
# index.check_if_indexing_is_good(index_type = Indexes.SUMMARIES.value)
index.store_index('./index/'+Indexes.STARS.value+'_index.json', Indexes.STARS.value)
index.store_index('./index/'+Indexes.SUMMARIES.value+'_index.json', Indexes.SUMMARIES.value)
index.store_index('./index/'+Indexes.GENRES.value+'_index.json', Indexes.GENRES.value)
index.store_index('./index/'+Indexes.DOCUMENTS.value+'_index.json', Indexes.DOCUMENTS.value)


# loaded = index.load_index('./stars.json')
# print(index.check_if_index_loaded_correctly(Indexes.STARS.value, loaded))