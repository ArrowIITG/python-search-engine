## Python search engine with TF-IDF ranking

This project following the general idea of this [blog post](http://aakashjapi.com/fuckin-search-engines-how-do-they-work/). A starting point implementation was given in Python and can be found [here](./original-src).

## Search engines

There are 3 major stages in developing a search engine:
1) Finding/Crawling the data
2) Building the index
3) Querying the index

> The final step in building a search engine is creating a system to rank documents by their relevance to the query. 
Here, we implemented tf-idf ranking (term frequency - inverse document frequency) to order our documents.
