## Python search engine with TF-IDF ranking

This project following the general idea of this [blog post](http://aakashjapi.com/fuckin-search-engines-how-do-they-work/). A starting point implementation was given in Python and can be found [here](./original-src).

## Search engines

There are 3 major stages in developing a search engine:
1) Finding/Crawling the Data
2) Building the index
3) Using the index to answer queries

> On top of this, we can add result ranking (tf-idf, PageRank, etc), query/document classification and maybe some Machine Learning to keep track of user's past queries and selected results to improve the search engine's performance.
