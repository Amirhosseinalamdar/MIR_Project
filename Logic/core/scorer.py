import numpy as np
from .indexer.index_reader import Index_reader
from .indexer.indexes_enum import Indexes, Index_types
class Scorer:    
    def __init__(self, index, number_of_documents):
        """
        Initializes the Scorer.

        Parameters
        ----------
        index : dict
            The index to score the documents with.
        number_of_documents : int
            The number of documents in the index.
        """

        self.index = index
        self.idf = {}
        self.N = number_of_documents

    def get_list_of_documents(self,query):
        """
        Returns a list of documents that contain at least one of the terms in the query.

        Parameters
        ----------
        query: List[str]
            The query to be scored

        Returns
        -------
        list
            A list of documents that contain at least one of the terms in the query.
        
        Note
        ---------
            The current approach is not optimal but we use it due to the indexing structure of the dict we're using.
            If we had pairs of (document_id, tf) sorted by document_id, we could improve this.
                We could initialize a list of pointers, each pointing to the first element of each list.
                Then, we could iterate through the lists in parallel.
            
        """
        list_of_documents = []
        for term in query:
            if term in self.index.keys():
                list_of_documents.extend(self.index[term].keys())
        return list(set(list_of_documents))
    
    def get_idf(self, term):
        """
        Returns the inverse document frequency of a term.

        Parameters
        ----------
        term : str
            The term to get the inverse document frequency for.

        Returns
        -------
        float
            The inverse document frequency of the term.
        
        Note
        -------
            It was better to store dfs in a separate dict in preprocessing.
        """
        idf = self.idf.get(term, None)
        if idf is None:
            if term in self.index:
                self.idf[term] = len(self.index[term]) # TODO what if new term
            else: 
                self.idf[term] = 0.1

            idf = self.idf[term]
        return idf
    
    def get_query_tfs(self, query):
        """
        Returns the term frequencies of the terms in the query.

        Parameters
        ----------
        query : List[str]
            The query to get the term frequencies for.

        Returns
        -------
        dict
            A dictionary of the term frequencies of the terms in the query.
        """
        
        res = dict()
        for qw in query:
            if qw in self.index:
                res[qw] = sum(self.index[qw].values())
            else:
                res[qw] = 0

    def compute_scores_with_vector_space_model(self, query, method):
        """
        compute scores with vector space model

        Parameters
        ----------
        query: List[str]
            The query to be scored
        method : str ((n|l)(n|t)(n|c).(n|l)(n|t)(n|c))
            The method to use for searching.

        Returns
        -------
        dict
            A dictionary of the document IDs and their scores.
        """

        doc_id_list = self.get_list_of_documents(query)

        if method[1] == 't' or method[5]=='t':
            idf_multiplier = np.zeros(len(self.index), dtype = float)
            for i, term in enumerate(self.index):
                idf_multiplier[i] = np.log(self.N / self.get_idf(term))

        X = np.zeros((len(self.index), len(doc_id_list)), dtype = float)
        for i, term in enumerate(self.index):
            for j, doc_id in enumerate(doc_id_list):
                if doc_id in self.index[term]:
                    if method[0] == 'n':
                        X[i, j] = self.index[term][doc_id]
                    elif method[0] == 'l':
                        X[i, j] = np.log(self.index[term][doc_id]) + 1
        
        if method[1] == 't':
            idf = idf_multiplier.reshape(-1, 1)
            X = X * idf

        if method[2] == 'c':
            X = X / np.linalg.norm(X, axis = 0)
        


        q = np.zeros(len(self.index), dtype=float)
        for i , term in enumerate(self.index):
            if term in query:
                if method[4] == 'n':
                    q[i] = query.count(term)
                elif method[4]=='l':
                    q[i] = np.log(query.count(term)) + 1

        if method[5] == 't':
            q = q * idf_multiplier
        
        if method[6] == 'c':
            if q.sum() > 0:
                q = q / np.linalg.norm(q)

        scores = (q @ X).tolist()

        return dict(zip(doc_id_list, scores))


    def get_vector_space_model_score(self, query, query_tfs, document_id, document_method, query_method):
        """
        Returns the Vector Space Model score of a document for a query.

        Parameters
        ----------
        query: List[str]
            The query to be scored
        query_tfs : dict
            The term frequencies of the terms in the query.
        document_id : str
            The document to calculate the score for.
        document_method : str (n|l)(n|t)(n|c)
            The method to use for the document.
        query_method : str (n|l)(n|t)(n|c)
            The method to use for the query.

        Returns
        -------
        float
            The Vector Space Model score of the document for the query.
        """
        ## implemented in the above function
        pass

    def okapi_score_tf(self, tf, dl_avgdl, b=0.75, k1 = 1.5):
        return (k1 + 1)*tf / (tf + k1*(1-b+b*dl_avgdl))
    
    def compute_scores_with_okapi_bm25(self, query, average_document_field_length, document_lengths):
        """
        compute scores with okapi bm25

        Parameters
        ----------
        query: List[str]
            The query to be scored
        average_document_field_length : float
            The average length of the documents in the index.
        document_lengths : dict
            A dictionary of the document lengths. The keys are the document IDs, and the values are
            the document's length in that field.
        
        Returns
        -------
        dict
            A dictionary of the document IDs and their scores.
        """

        doc_id_list = self.get_list_of_documents(query)
    
        idf_multiplier = np.zeros(len(query), dtype = float)
        for i, term in enumerate(query):
            idf_multiplier[i] = np.log(self.N / self.get_idf(term))

        X = np.zeros((len(query), len(doc_id_list)), dtype = float)
        for i, term in enumerate(query):
            if term not in self.index:
                continue
            for j, doc_id in enumerate(doc_id_list):
                if doc_id in self.index[term]:
                    X[i, j] = self.okapi_score_tf(self.index[term][doc_id], document_lengths[doc_id] / average_document_field_length)
        
        idf = idf_multiplier.reshape(-1, 1)
        X = X * idf
        scores = X.sum(axis = 0)

        return dict(zip(doc_id_list, scores))
        
    def get_okapi_bm25_score(self, query, document_id, average_document_field_length, document_lengths):
        """
        Returns the Okapi BM25 score of a document for a query.

        Parameters
        ----------
        query: List[str]
            The query to be scored
        document_id : str
            The document to calculate the score for.
        average_document_field_length : float
            The average length of the documents in the index.
        document_lengths : dict
            A dictionary of the document lengths. The keys are the document IDs, and the values are
            the document's length in that field.

        Returns
        -------
        float
            The Okapi BM25 score of the document for the query.
        """
        # IMPLEMENTED IN THE ABOVE FUNCTION
        pass

# ================================ = = = = = = = = = = = = = = =====================================

# docs_index = Index_reader('./indexer/index/', Indexes.SUMMARIES).index
# doc_len = Index_reader('./indexer/index/', Indexes.SUMMARIES, Index_types.DOCUMENT_LENGTH).index

# sc = Scorer(docs_index, len(docs_id_index))

# # dictionary = sc.compute_scores_with_vector_space_model(['bad', 'fight'], 'ltc.ltc')
# dictionary = sc.compute_scores_with_okapi_bm25(['bad', 'fight'], 409.49, doc_len)



# sorted_items = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
# top_5 = sorted_items[:5]

# docs_id_index = Index_reader('index/', Indexes.DOCUMENTS).index
# print(top_5)

# docs_id_index = Index_reader('./indexer/index/', Indexes.DOCUMENTS).index
# print(docs_id_index[top_5[0][0]][Indexes.SUMMARIES.value])

