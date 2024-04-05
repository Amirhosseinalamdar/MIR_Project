import streamlit as st
import sys

sys.path.append("../")
from Logic import utils
import time
from enum import Enum
import random
<<<<<<< HEAD
=======
from Logic.core.snippet import Snippet

snippet_obj = Snippet(
    number_of_words_on_each_side=5
)  # You can change this parameter, if needed.
>>>>>>> template/main


class color(Enum):
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"
    YELLOW = "#FFFF00"
<<<<<<< HEAD
=======
    WHITE = "#FFFFFF"
    CYAN = "#00FFFF"
    MAGENTA = "#FF00FF"


def get_summary_with_snippet(movie_info, query):
    summary = movie_info["first_page_summary"]
    snippet, not_exist_words = snippet_obj.find_snippet(summary, query)
    if "***" in snippet:
        snippet = snippet.split()
        for i in range(len(snippet)):
            current_word = snippet[i]
            if current_word.startswith("***") and current_word.endswith("***"):
                current_word_without_star = current_word[3:-3]
                summary = summary.lower().replace(
                    current_word_without_star,
                    f"<b><font size='4' color={random.choice(list(color)).value}>{current_word_without_star}</font></b>",
                )
    return summary
>>>>>>> template/main


def search_time(start, end):
    st.success("Search took: {:.6f} milli-seconds".format((end - start) * 1e3))


def search_handling(
    search_button,
<<<<<<< HEAD
    search_title_terms,
    search_summary_terms,
    search_max_num,
    search_weight,
    search_method,
):
    if search_button:
        corrected_title = utils.correct_text(search_title_terms, utils.bigram_index)
        corrected_abstract = utils.correct_text(
            search_summary_terms, utils.bigram_index
        )
        corrected = corrected_title + " " + corrected_abstract

        if (
            corrected_title != search_title_terms
            or corrected_abstract != search_summary_terms
        ):
            st.warning(f"Your search terms were corrected to: {corrected}")
            search_title_terms = corrected_title
            search_summary_terms = corrected_abstract
=======
    search_term,
    search_max_num,
    search_weights,
    search_method,
):
    if search_button:
        corrected_query = utils.correct_text(search_term, utils.movies_dataset)

        if corrected_query != search_term:
            st.warning(f"Your search terms were corrected to: {corrected_query}")
            search_term = corrected_query
>>>>>>> template/main

        with st.spinner("Searching..."):
            time.sleep(0.5)  # for showing the spinner! (can be removed)
            start_time = time.time()
            result = utils.search(
<<<<<<< HEAD
                search_title_terms,
                search_summary_terms,
                search_max_num,
                search_method,
                search_weight,
            )
=======
                search_term,
                search_max_num,
                search_method,
                search_weights,
            )
            print(f"Result: {result}")
>>>>>>> template/main
            end_time = time.time()
            if len(result) == 0:
                st.warning("No results found!")
                return

            search_time(start_time, end_time)

            for i in range(len(result)):
                card = st.columns([3, 1])
                info = utils.get_movie_by_id(result[i][0], utils.movies_dataset)
                with card[0].container():
<<<<<<< HEAD
                    st.title(info["Title"])
                    st.markdown(f"[Link to movie]({info['URL']})")
                    st.write(f"Relevance Score: {result[i][1]}")
                    st.write(info["Summary"])
                    with st.expander("Cast"):
                        num_authors = len(info["Cast"])

                        for j in range(num_authors):
                            st.write(info["Cast"][j])
=======
                    st.title(info["title"])
                    st.markdown(f"[Link to movie]({info['URL']})")
                    st.write(f"Relevance Score: {result[i][1]}")
                    st.markdown(
                        f"<b><font size = '4'>Summary:</font></b> {get_summary_with_snippet(info, search_term)}",
                        unsafe_allow_html=True,
                    )

                with st.container():
                    st.markdown("**Directors:**")
                    num_authors = len(info["directors"])
                    for j in range(num_authors):
                        st.text(info["directors"][j])

                with st.container():
                    st.markdown("**Stars:**")
                    num_authors = len(info["stars"])
                    stars = "".join(star + ", " for star in info["stars"])
                    st.text(stars[:-2])
>>>>>>> template/main

                    topic_card = st.columns(1)
                    with topic_card[0].container():
                        st.write("Genres:")
<<<<<<< HEAD
                        num_topics = len(info["Genres"])
                        for j in range(num_topics):
                            st.markdown(
                                f"<span style='color:{random.choice(list(color)).value}'>{info['Genres'][j]}</span>",
=======
                        num_topics = len(info["genres"])
                        for j in range(num_topics):
                            st.markdown(
                                f"<span style='color:{random.choice(list(color)).value}'>{info['genres'][j]}</span>",
>>>>>>> template/main
                                unsafe_allow_html=True,
                            )
                with card[1].container():
                    st.image(info["Image_URL"], use_column_width=True)

                st.divider()


def main():
    st.title("Search Engine")
    st.write(
        "This is a simple search engine for IMDB movies. You can search through IMDB dataset and find the most relevant movie to your search terms."
    )
    st.markdown(
        '<span style="color:yellow">Developed By: MIR Team at Sharif University</span>',
        unsafe_allow_html=True,
    )

<<<<<<< HEAD
    search_title_terms = st.text_input("Seacrh in title")
    search_summary_terms = st.text_input("Search in summary of movie")
=======
    search_term = st.text_input("Seacrh Term")
    # search_summary_terms = st.text_input("Search in summary of movie")
>>>>>>> template/main
    with st.expander("Advanced Search"):
        search_max_num = st.number_input(
            "Maximum number of results", min_value=5, max_value=100, value=10, step=5
        )
<<<<<<< HEAD
        search_weight = st.slider(
            "Weight of title in search",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1,
        )
        search_method = st.selectbox(
            "Search method",
            ("ltn-lnn", "ltc-lnc", "okapi25"),
=======
        weight_stars = st.slider(
            "Weight of stars in search",
            min_value=0.0,
            max_value=1.0,
            value=1.0,
            step=0.1,
        )

        weight_genres = st.slider(
            "Weight of genres in search",
            min_value=0.0,
            max_value=1.0,
            value=1.0,
            step=0.1,
        )

        weight_summary = st.slider(
            "Weight of summary in search",
            min_value=0.0,
            max_value=1.0,
            value=1.0,
            step=0.1,
        )

        search_weights = [weight_stars, weight_genres, weight_summary]
        search_method = st.selectbox(
            "Search method",
            ("ltn.lnn", "ltc.lnc", "OkapiBM25"),
>>>>>>> template/main
        )

    search_button = st.button("Search!")

    search_handling(
        search_button,
<<<<<<< HEAD
        search_title_terms,
        search_summary_terms,
        search_max_num,
        search_weight,
=======
        search_term,
        search_max_num,
        search_weights,
>>>>>>> template/main
        search_method,
    )


if __name__ == "__main__":
    main()
