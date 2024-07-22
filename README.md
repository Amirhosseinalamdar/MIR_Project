# IMDB Search Engine for MIR course
#### There are plenty of details in these three phases which are ignored to be as short and simple as possible.
## Phase 1: Traditional Search Engine Implementation
* Crawled IMDB to collect data for the search engine. (id, title, link, similar links, MPA, starts, directors, budget, genres, and ... for each movie. around 1000 movie for this phase and 10k for the next phase)
* Developed search engine using traditional methods: Vector Space Model | Okapi BM25 | Unigram Language Model        
* Implemented LSG min hash to identify duplicate documents in O(n).
* Implemented spell correction using crawled text data and singling and jacard similarity method. (also ranking candidates based on tf)
* Also, evaluating results using retrieval metrics and extracting a snippet for each document given the query.
  
## Phase 2: Enhanced Search Results and Content Classification     
* Link Analysis: Applied hub and authority scores to improve search results. (HITS algorithm)
* Text Embedding: Trained a FastText model for text embeddings. (Skip gram)
* Content Classification: Developed and evaluated multiple classifiers to categorize content: Support Vector Machine | Naive Bayes | K-Nearest Neighbors | Deep model
* Clustering Utilities: Performed several clustering methods on text embeddings to group similar content.
## Phase 3: RAG, Bert, Recommender system
this phase contained three jupyter notebooks and was independent of the final search engine:
* RAG and LLM: Used Langchain and Hugginface to feed 10 retrieved documents as context to the LLM model and user prompt. Finally, returning the llm answer to the user given this template. Also, the user prompt is expanded before going into the template, using another llm.
* Recommender System: multiple algorithms like content-based, Collaborative filtering, and PCA to predict the user ratings of different movies.
* Bert: Finetuning Bert for the genre classification task. (MLM) 


https://github.com/user-attachments/assets/61861608-44c3-4efc-acba-e269c91c8e2b











# MIR-2024-Project-template
<img src="./IMDB_Logo.jpeg" alt="IMDb Logo" width="100%" height="auto" />
This is the repository for Modern Information Retrieval Course, Instructed by Dr. Mahdieh Soleymani Baghshah at Sharif University of Technology.

## What is this project about?
One of the ways to compare movies and understand which one is a better choice for you, is through websites with this purpose and using appropriate information retrieval methods.

In this phase of project, we begin our journey towards building an information retrieval system for [IMDb](https://www.imdb.com/) website. In this phase, we crawl the required datas from [IMDb](https://www.imdb.com/) and do some preprocessing on them. [IMDb](https://www.imdb.com/) has one of the reachest datasets of movies (with their ratings, comments, actors and etc.).

## A note on forking this repository
You should make a **private** repository in your personal github account in order to push your answers and also, for TAs being able to track your work. Please choose `Use this Template` in this repository and choose `Create a new repository`. Make sure you make your repository **private**.

In order to be able to get the new changes and files from our main repository into your own repository, you should add this repository as a remote:
```bash
git remote add template [URL of the template repo]
```
and then, you can simply run `git fetch` to update the changes whenever you want:
```bash
git fetch --all
```

## General Structure
The project contains 2 main modules: [Logic](./Logic/README.md) and [UI](./UI/README.md). The `Logic` module is responsible for doing the main tasks of the project and the `UI` module is responsible for providing a user interface for the user to interact with the system. In each task, you will be told to implement a part or a whole file in one of these modules. Please read the comments for each file and functions inside it to understand what you need to do.






#### phase 2 link:

https://drive.google.com/file/d/1tYZwLzzMp7295dvWoNXfxFr6WhlcM05I/view?usp=sharing
(remember argparsers)

#### phase 3 link:
https://drive.google.com/drive/folders/13O_4oETdIfpHhhbam1Rb3ttyEHDc4I8i?usp=sharing


#### improved UI/UX
https://drive.google.com/file/d/1LhovzsnmWOuc3QYO2dA6un4vdfrmsOF_/view?usp=sharing



