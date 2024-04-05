import re
import nltk
from nltk.stem import WordNetLemmatizer

class Preprocessor:

    def __init__(self, documents: list, path='./stopwords.txt'):
        """
        Initialize the class.

        Parameters
        ----------
        documents : list
            The list of documents to be preprocessed, path to stop words, or other parameters.
        """
        # TODO
        self.documents = documents
        self.stopwords = []

        with open(path, 'r') as file:
            for line in file:
                self.stopwords.append(line.strip())

    def preprocess(self):
        """
        Preprocess the text using the methods in the class.

        Returns
        ----------
        str
            The preprocessed documents.
        """
        #  1 remove links
        #  2 remove puncts
        #  3 normalize
        prep = []
        for doc in self.docs:
            doc = self.remove_links(doc)
            doc = self.remove_puctuations(doc)
            doc = self.normalize(doc)
            prep.append(doc)
            
        return prep

    def normalize(self, text: str):
        """
        Normalize the text by converting it to a lower case, stemming, lemmatization, etc.

        Parameters
        ----------
        text : str
            The text to be normalized.

        Returns
        ----------
        str
            The normalized text.
        """
        # to lowercase and remove stop words and do lemmatization
        text =text.lower()
        tokens = self.remove_stopwords(text)

        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

        return ' '.join(lemmatized_tokens)



    def remove_links(self, text: str):
        """
        Remove links from the text.

        Parameters
        ----------
        text : str
            The text to be processed.

        Returns
        ----------
        str
            The text with links removed.
        """
        patterns = [r'\S*http\S*', r'\S*www\S*', r'\S+\.ir\S*', r'\S+\.com\S*', r'\S+\.org\S*', r'\S*@\S*']
        compiled_patterns = [re.compile(pattern) for pattern in patterns]
        cleaned_text = text
        for pattern in compiled_patterns:
            cleaned_text = pattern.sub('', cleaned_text)
        
        return cleaned_text


    def remove_punctuations(self, text: str):
        """
        Remove punctuations from the text.

        Parameters
        ----------
        text : str
            The text to be processed.

        Returns
        ----------
        str
            The text with punctuations removed.
        """
        punctuation_pattern = r'[^\w\s]'  
        return re.sub(punctuation_pattern, ' ', text)

    def tokenize(self, text: str):
        """
        Tokenize the words in the text.

        Parameters
        ----------
        text : str
            The text to be tokenized.

        Returns
        ----------
        list
            The list of words.
        """
        # TODO
        return text.split()

    def remove_stopwords(self, text: str):
        """
        Remove stopwords from the text.

        Parameters
        ----------
        text : str
            The text to remove stopwords from.

        Returns
        ----------
        list
            The list of words with stopwords removed.
        """
        words = self.tokenize(text) 
        return [word for word in words if word.lower() not in self.stopwords]

