import re
import string
import typing

import contractions
import sklearn.feature_extraction.text
from nltk import PorterStemmer, RegexpTokenizer
from nltk.corpus import stopwords
from pydantic import BaseModel
import nltk
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

from DataModel import DataModel

ModelRegressor = typing.Union[LinearSVC, MultinomialNB, RandomForestClassifier, LogisticRegression,
                              DecisionTreeClassifier]


def process_text(text):
    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('english')
    # Lower case
    text = text.lower()
    # Remove tags
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
    # Remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)
    # Remove hyperlinks
    text = re.sub(r'https?://[^\s\n\r]+', '', text)
    # only removing the hash # sign from the word
    text = re.sub(r'#', '', text)
    # Contractions
    text = contractions.fix(text)
    # Tokenize text
    tokenizer = RegexpTokenizer(r'\w+')
    texts_tokens = tokenizer.tokenize(text)

    texts_clean = []
    for word in texts_tokens:
        if (word not in stopwords_english and  # remove stopwords
                word not in string.punctuation):  # remove punctuation
            stem_word = stemmer.stem(word)  # stemming word
            texts_clean.append(stem_word)

    return texts_clean


class PredictionModel:
    model: ModelRegressor
    tfidf_vectorizer: sklearn.feature_extraction.text.TfidfVectorizer
    fs: SelectFromModel

    def __init__(self):
        self.model = pickle.load(open('models/model_lr.pkl', 'rb'))
        self.tfidf_vectorizer = pickle.load(open('models/tfidf_vectorizer.pkl', 'rb'))
        self.fs = pickle.load(open('models/feature_selection.pkl', 'rb'))
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')

    def predict(self, text):
        orig_text = text
        text = process_text(text)
        text = ' '.join(map(str, text))
        text = [text]
        text = self.tfidf_vectorizer.transform(text)
        prediction = self.model.predict(text)[0]
        if prediction == 0:
            return {
                "response": "nosuicide",
                "original_input": orig_text
            }
        else:
            return {
                "response": "suicide",
                "original_input": orig_text
            }

        #return self.test_predict(data)

    def test_predict(self, data: str):
        if len(data) < 10:
            return {
                "response": "suicide",
                "original_input": data
            }
        else:
            return {
                "response": "nosuicide",
                "original_input": data
            }

    def make_predictions(self, data: DataModel):
        result = self.predict(data.text)
        return result
