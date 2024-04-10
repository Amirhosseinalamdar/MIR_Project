import numpy as np
import json
class SpellCorrection:
    def __init__(self, all_documents):
        """
        Initialize the SpellCorrection

        Parameters
        ----------
        all_documents : list of str
            The input documents.
        """
        self.all_shingled_words, self.word_counter = self.shingling_and_counting(all_documents)

    def shingle_word(self, word, k=2):
        """
        Convert a word into a set of shingles.

        Parameters
        ----------
        word : str
            The input word.
        k : int
            The size of each shingle.

        Returns
        -------
        set
            A set of shingles.
        """
        word = '$' + word + '$'
        shingles = set()
        for i in range(len(word)-1):
            shingles.add(word[i:i+2])
        return shingles
    
    def jaccard_score(self, first_set, second_set):
        """
        Calculate jaccard score.

        Parameters
        ----------
        first_set : set
            First set of shingles.
        second_set : set
            Second set of shingles.

        Returns
        -------
        float
            Jaccard score.
        """

        # TODO: Calculate jaccard score here.
        return len(first_set.intersection(second_set)) / len(first_set.union(second_set))

    def shingling_and_counting(self, all_documents):
        """
        Shingle all words of the corpus and count TF of each word.

        Parameters
        ----------
        all_documents : list of str
            The input documents.

        Returns
        -------
        all_shingled_words : dict
            A dictionary from words to their shingle sets.
        word_counter : dict
            A dictionary from words to their TFs.
        """
        all_shingled_words = dict()
        word_counter = dict()

        # TODO: Create shingled words dictionary and word counter dictionary here.
        for doc in all_documents:
            for term in doc.split():
                if term not in all_shingled_words:
                    all_shingled_words[term] = self.shingle_word(term)
                if term not in word_counter:
                    word_counter[term] = 0
                word_counter[term] += 1
    
        return all_shingled_words, word_counter
    
    def find_nearest_words(self, word):
        """
        Find correct form of a misspelled word.

        Parameters
        ----------
        word : stf
            The misspelled word.

        Returns
        -------
        list of str
            5 nearest words.
        """

        scores = np.zeros(len(self.word_counter))
        words = np.array(list(self.word_counter.keys()))
        
        for i, term in enumerate(words):
            scores[i] = self.jaccard_score(self.all_shingled_words[term], self.shingle_word(word))
        
        sorted_indices_desc = np.argsort(-scores)
        top_k_indices = sorted_indices_desc[:5]

        unNormalized = scores[top_k_indices]
        
        topk_words = words[top_k_indices]
        topk_tf = np.array([self.word_counter[term] for term in topk_words])
        topk_tf = topk_tf / topk_tf.max()

        normalized = unNormalized * topk_tf

        return topk_words[np.argsort(-normalized)].tolist()
    
    def spell_check(self, query):
        """
        Find correct form of a misspelled query.

        Parameters
        ----------
        query : stf
            The misspelled query.

        Returns
        -------
        str
            Correct form of the query.
        """
        # final_result = ""
        final_result = self.find_nearest_words(query)
        # TODO: Do spell correction here.
        return final_result
    



# from indexer.index_reader import Index_reader
# from  indexer.indexes_enum import Indexes
# index_docs = Index_reader('./indexer/index/', index_name=Indexes.DOCUMENTS).index

# docs = []
# for id in index_docs:
#     docs.append(' '.join(index_docs[id]['summaries']))

# file_path = "spell_correction_data.json"

# with open(file_path, "w") as json_file:
#     json.dump(docs, json_file)