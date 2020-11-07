![CI Status](https://github.com/michdr/satzify/workflows/CI/badge.svg)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/michdr/satzify/main/app.py)

# satzify
> Simple sentences annotator

Satzify is a small web app built using [streamlit](https://www.streamlit.io/).
Its NLP batteries are powered by [spaCy](https://spacy.io/).
The main use case it to quickly annotate sentences in German with a focus on parts of speech, cases and the respective genders in that context.
From some observations, the results that it gives are not 100% correct. For some longer or ambiguous sentences there might be mistakes. Nevertheless, for the sake of learning the language and quickly checking various sentences it's alright.

![Demo](https://raw.githubusercontent.com/michdr/satzify/main/demo.gif "Demo")

## Installing
In a venv:
```bash
pip install -r requirements.txt
``` 

## Testing
Additionally to the above:
```bash
pip install -r requirements-dev.txt
pytest tests/*.py
``` 

## Running
Locally:
```bash
streamlit run app.py
``` 
Or simply via [streamlit sharing](https://share.streamlit.io/michdr/satzify/main/app.py)
