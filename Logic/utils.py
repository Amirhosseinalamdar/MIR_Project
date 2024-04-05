from typing import Dict, List
<<<<<<< HEAD
from .core.preprocess import Preprocessor

bigram_index = None
movies_dataset = None
preprocessor = ... # TODO

def clean_query(query: str) -> str:
    """
    Cleans the given query using preprocessor

    Parameters
    ----------
    query: str
        The query text
    
    Returns
    str
        The cleaned and pre-processed form of the given query
    """
    # TODO
    return query

def correct_text(
    text: str, bigram_index: Dict[str, List[str]], similar_words_limit: int = 20
) -> str:
=======
from core.search import SearchEngine
from core.spell_correction import SpellCorrection
from core.snippet import Snippet
from core.indexes_enum import Indexes, Index_types
import json

movies_dataset = None  # TODO
search_engine = SearchEngine()


def correct_text(text: str, all_documents: List[str]) -> str:
>>>>>>> template/main
    """
    Correct the give query text, if it is misspelled using Jacard similarity

    Paramters
    ---------
    text: str
        The query text
<<<<<<< HEAD
=======
    all_documents : list of str
        The input documents.
>>>>>>> template/main

    Returns
    str
        The corrected form of the given text
    """
<<<<<<< HEAD
    cleaned_text = clean_query(text)
    # ...
    return cleaned_text


def search(
    title_query: str,
    abstract_query: str,
    max_result_count: int,
    method: str = "ltn-lnn",
    weight: float = 0.5,
    should_print=False,
    preferred_field: str = None,
=======
    # TODO: You can add any preprocessing steps here, if needed!
    spell_correction_obj = SpellCorrection(all_documents)
    text = spell_correction_obj.spell_check(text)
    return text


def search(
    query: str,
    max_result_count: int,
    method: str = "ltn-lnn",
    weights: list = [0.3, 0.3, 0.4],
    should_print=False,
    preferred_genre: str = None,
>>>>>>> template/main
):
    """
    Finds relevant documents to query

    Parameters
    ---------------------------------------------------------------------------------------------------
    max_result_count: Return top 'max_result_count' docs which have the highest scores.
                      notice that if max_result_count = -1, then you have to return all docs

    mode: 'detailed' for searching in title and text separately.
          'overall' for all words, and weighted by where the word appears on.

    where: when mode ='detailed', when we want search query
            in title or text not both of them at the same time.

<<<<<<< HEAD
    method: 'ltn-lnn' or 'ltc-lnc' or 'okapi25'

    preferred_field: A list containing preference rates for each field. If None, the preference rates are equal.
=======
    method: 'ltn.lnn' or 'ltc.lnc' or 'OkapiBM25'

    preferred_genre: A list containing preference rates for each genre. If None, the preference rates are equal.
>>>>>>> template/main

    Returns
    ----------------------------------------------------------------------------------------------------
    list
    Retrieved documents with snippet
    """
<<<<<<< HEAD
    return ["1243523", "6753495", "2342348"]
=======
    weights = ...  # TODO
    return search_engine.search(
        query, method, weights, max_results=max_result_count, safe_ranking=True
    )
>>>>>>> template/main


def get_movie_by_id(id: str, movies_dataset: List[Dict[str, str]]) -> Dict[str, str]:
    """
    Get movie by its id

    Parameters
    ---------------------------------------------------------------------------------------------------
    id: str
        The id of the movie

    movies_dataset: List[Dict[str, str]]
        The dataset of movies

    Returns
    ----------------------------------------------------------------------------------------------------
    dict
        The movie with the given id
    """
<<<<<<< HEAD

    return {
        "Title": "This is movie's title",
        "Summary": "This is a summary",
        "URL": "https://www.imdb.com/title/tt0111161/",
        "Cast": ["Morgan Freeman", "Tim Robbins"],
        "Genres": ["Drama", "Crime"],
        "Image_URL": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg",
    }
=======
    result = movies_dataset.get(
        id,
        {
            "Title": "This is movie's title",
            "Summary": "This is a summary",
            "URL": "https://www.imdb.com/title/tt0111161/",
            "Cast": ["Morgan Freeman", "Tim Robbins"],
            "Genres": ["Drama", "Crime"],
            "Image_URL": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg",
        },
    )

    result["Image_URL"] = (
        "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg"  # a default picture for selected movies
    )
    result["URL"] = (
        f"https://www.imdb.com/title/{result['id']}"  # The url pattern of IMDb movies
    )
    return result
>>>>>>> template/main
