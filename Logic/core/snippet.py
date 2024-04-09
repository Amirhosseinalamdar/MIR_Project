import numpy as np
class Snippet:
    def __init__(self, number_of_words_on_each_side=5):
        """
        Initialize the Snippet

        Parameters
        ----------
        number_of_words_on_each_side : int
            The number of words on each side of the query word in the doc to be presented in the snippet.
        """
        self.n = number_of_words_on_each_side

    def remove_stop_words_from_query(self, query, path = './stopwords.txt'):
        """
        Remove stop words from the input string.

        Parameters
        ----------
        query : str
            The query that you need to delete stop words from.

        Returns
        -------
        str
            The query without stop words.
        """
        stopwords = []
        
        with open(path, 'r') as file:
            for line in file:
                stopwords.append(line.strip())
        query = [word for word in query.split() if word not in stopwords]
        return ' '.join(query)

    def find_snippet(self, doc, query):
        """
        Find snippet in a doc based on a query.

        Parameters
        ----------
        doc : str
            The retrieved doc which the snippet should be extracted from that.
        query : str
            The query which the snippet should be extracted based on that.

        Returns
        -------
        final_snippet : str
            The final extracted snippet. IMPORTANT: The keyword should be wrapped by *** on both sides.
            For example: Sahwshank ***redemption*** is one of ... (for query: redemption)
        not_exist_words : list
            Words in the query which don't exist in the doc.
        """
        # Have removed stopwords from query in this method
        query = self.remove_stop_words_from_query(query)
        final_snippet = ""
        not_exist_words = []
        snippets = []
        query_lst = query.split()
        doc_lst = doc.split()

        if len(doc.split()) < 2*self.n + 1:
            return None, None #TODO JEEZ

        for qw in query_lst:
            if qw in doc_lst:
                index = doc_lst.index(qw)
                if index < self.n:
                    curr = doc_lst[:index+self.n+1]
                elif len(doc_lst)-index <= self.n:
                    curr = doc_lst[index-self.n:]
                else:
                    curr = doc_lst[index-self.n:index+self.n+1]
                index = curr.index(qw)
                curr[index] = '***'+curr[index]+'***'
                snippets.append(' '.join(curr))
            else:
                not_exist_words.append(qw)

        final_snippet = '...'.join(snippets)
        return final_snippet, not_exist_words


# VALIDATED