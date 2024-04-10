import numpy as np
import itertools
import random
from random import shuffle

import json

class MinHashLSH:
    def __init__(self, documents, num_hashes):
        """
        Initialize the MinHashLSH

        Parameters
        ----------
        documents : list of str
            The input documents for similarity analysis.
        num_hashes : int
            Number of hashes for mini-hashing.
        """
        self.documents = documents
        self.num_hashes = num_hashes

    def shingle_document(self, document, k=2):
        """
        Convert a document into a set of shingles.

        Parameters
        ----------
        document : str
            The input document.
        k : int
            The size of each shingle.

        Returns
        ----------
        set
            A set of shingles.
        """
        shingles = set()
        # can just do shingling on the raw sentence and not splitting the words TODO later
        doc = document.split()
        for i in range(len(doc) - k + 1):
            shingles.add(' '.join(doc[i:i+k]))
        return shingles

        # for i in range(len(document) - k + 1):
        #     shingles.add(document[i:i+k])
        # return shingles

    def build_characteristic_matrix(self):
        """
        Build the characteristic matrix representing the presence of shingles in documents.

        Returns
        ----------
        numpy.ndarray
            The binary characteristic matrix.
        """
        shingles_lst = []
        all_shingles = set()
        for doc in self.documents:
            shingles =self.shingle_document(doc)
            all_shingles = all_shingles.union(shingles)
            shingles_lst.append(shingles)

        N = len(all_shingles)
        M = len(self.documents)
        matrix = np.zeros((N, M), dtype=int)

        for i, sh in enumerate(all_shingles):
            for j, shingles_set in enumerate(shingles_lst):
                if sh in shingles_set:
                    matrix[i, j] = 1
        
        return matrix

    def min_hash_signature(self):
        """
        Perform Min-Hashing to generate hash signatures for documents.

        Returns
        ----------
        numpy.ndarray
            The Min-Hash signatures matrix.
        """
        
        matrix = self.build_characteristic_matrix()
        
        sig_matrix = np.full((self.num_hashes, matrix.shape[1]), np.inf)
        hash_functions = [np.random.permutation(matrix.shape[0]) for _ in range(self.num_hashes)]
        
        for doc in range(matrix.shape[1]):
            for j, hash in enumerate(hash_functions):
                tmp = np.where(matrix[hash, doc]==1)[0]
                if len(tmp) > 0:
                    sig_matrix[j, doc] = min(np.where(matrix[hash, doc]==1)[0])

        return sig_matrix
    
  

    def lsh_buckets(self, signature, bands= 10, rows_per_band=10):
        """
        Group documents into Locality-Sensitive Hashing (LSH) buckets based on Min-Hash signatures.

        Parameters
        ----------
        signature : numpy.ndarray
            Min-Hash signatures for documents.
        bands : int
            Number of bands for LSH.
        rows_per_band : int
            Number of rows per band.

        Returns
        ----------
        dict
            A dictionary mapping bucket IDs to lists of document indices.
        """
        buckets = {}
        for band_idx in range(bands):
            band = signature[band_idx * rows_per_band : (band_idx + 1) * rows_per_band, :]
            band_transpose = band.T
            for dox_idx, row in enumerate(band_transpose):
                buckets.setdefault(hash((tuple(row), band_idx)), []).append(dox_idx)
        
        return buckets 

    def perform_lsh(self):
        """
        Perform the entire Locality-Sensitive Hashing (LSH) process.

        Returns
        ----------
        dict
            A dictionary mapping bucket IDs to lists of document indices.
        """
        sig_mat = self.min_hash_signature()
        return self.lsh_buckets(sig_mat)

    def jaccard_score(self, first_set, second_set):
        """
        Calculate jaccard score for two sets.

        Parameters
        ----------
        first_set : set
            Set of first shingled document.
        second_set : set
            Set of second shingled document.

        Returns
        ----------
        float
            Jaccard score.
        """
        intersection = len(first_set.intersection(second_set))
        union = len(first_set.union(second_set))
        jaccard_score = intersection / union if union != 0 else 0.0
        return jaccard_score


    def jaccard_similarity_test(self, buckets, all_documents):
        """
        Test your near duplicate detection code based on jaccard similarity.

        Parameters
        ----------
        buckets : dict
            A dictionary mapping bucket IDs to lists of document indices.
        all_documents : list
            The input documents for similarity analysis.
        """
        correct_near_duplicates = 0
        all_near_duplicates = 0

        for bucket_id in buckets.keys():
            docs_in_this_bucket = buckets[bucket_id]
            unique_doc_ids = set(docs_in_this_bucket)
            if len(unique_doc_ids) > 1:
                combinations = list(itertools.combinations(unique_doc_ids, 2))
                for comb in combinations:
                    all_near_duplicates += 1

                    first_doc_id = comb[0]
                    second_doc_id = comb[1]

                    first_shingled_doc = self.shingle_document(all_documents[first_doc_id], 2)
                    second_shingled_doc = self.shingle_document(all_documents[second_doc_id], 2)

                    near_duplicated_jaccard_score = self.jaccard_score(first_shingled_doc, second_shingled_doc)
                    current_score = 0

                    for _ in range(5):
                        random_doc_id = first_doc_id
                        while random_doc_id == first_doc_id or random_doc_id == second_doc_id:
                            random_doc_id = random.randint(0, len(all_documents) - 1)
                        random_shingled_doc = self.shingle_document(all_documents[random_doc_id], 2)

                        random_jaccard_score = self.jaccard_score(first_shingled_doc, random_shingled_doc)

                        if near_duplicated_jaccard_score > random_jaccard_score:
                            current_score += 1

                    if current_score == 5:
                        correct_near_duplicates += 1

        # a good score is around 0.8
        print("your final score in near duplicate detection:", correct_near_duplicates / all_near_duplicates)



file_path = "LSHFakeData.json"
with open(file_path, "r") as json_file:
    loaded_list = json.load(json_file)

with open('../IMDB_crawled.json', "r") as json_file:
    loaded_list.extend(json.load(json_file))


docs = []
for movie in loaded_list:
    docs.append(' '.join(movie['summaries']))

lsh = MinHashLSH(docs[:100],  100)

buckets = lsh.perform_lsh()

lsh.jaccard_similarity_test(buckets, docs)