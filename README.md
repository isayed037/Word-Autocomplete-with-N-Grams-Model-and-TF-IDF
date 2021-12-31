# Word-Autocomplete-with-N-Grams-Model-and-TF-IDF

Creates N-Gram model and TF-IDF model from any corpus in the “corpus” folder with different documents. Predict the next word in a sentence by calculating the Linear Interpolation using the Trigram model. At the end of a sentence calculates the Cosine Similarity using the TF-IDF model to find the document that is most similar to the sentence so far.

## Running and requirements

Run `main.py` to run the application.
All file imports are in `main.py` and `auto_complete_and_TF_IDF.py`.

All corpus are from https://www.english-corpora.org/corpora.asp

## Features

- Given any two words, predicts the next word. Shows the top 3 words with the highest probability.
- Uses a Trigram model with linear interpolation to predict the next word. Can predict the first word or the second word on an sentence. When given 2 words it can predict the 3rd word.
- Uses TF-IDF to find the most similar document. When you end a sentence with (".", ";", "?", "!"), uses that sentence to find the most similar document. Uses the most similar document for all future linear interpolation.
- Can create models from the `corpus` folder. Each folder in the `corpus` represents a document. A Trigram model will be created using all the `.txt` files in each individual documents. Another Trigram model will also be created using all documents.
- Can save all models and their information to the `model` folder. This will override all previous models in the folder and create new files for the new models.
- Can create models from the `model` folder. This is much faster than going through the entire corpus again and creating the same models.

### Contributions

If you have any ideas or contributions, feel free to create a pull request.
