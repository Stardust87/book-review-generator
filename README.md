# book-review-generator
This project uses GPT-2 architecture to generate book reviews given its category (positive or negative) and additional keywords. 

Data can be downloaded with scripts in ```webscraping``` directory. Information about books is obtained via Goodreads API, but users' reviews have to be webscraped. Multi-threading was used to speed up this process. 
After converting the data to csv format, it can be encoded in a special form that allows the GPT-2 model to learn keywords and categories of reviews (inspired by [this](https://github.com/minimaxir/gpt-2-keyword-generation)). Training pipeline and example results can be found in the notebook in ```modelling/nlp/``` .

## Authors

Project was made by Michał Szachniewicz ([szacho](https://github.com/szacho)) and Anna Klimiuk ([Stardust87](https://github.com/Stardust87)).
