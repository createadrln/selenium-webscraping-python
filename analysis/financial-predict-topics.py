import numpy as np
import pandas as pd

from atom import ATOMClassifier
from sklearn.datasets import fetch_20newsgroups
import matplotlib.pyplot as plt

import json
import csv
import os
import glob

# Load the dataset (get only 5 topics)
# X, y = fetch_20newsgroups(
#     return_X_y=True,
#     categories=[
#         'alt.atheism',
#         'sci.med',
#         'comp.windows.x',
#         'misc.forsale',
#         'rec.autos',
#     ],
# )

titles = []
urls = []
dates = []
pubs = []
content = []

with open('data-files/financial-blogs-data/combined.csv', encoding="utf8") as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
      
    for row in plots:
        titles.append(row[0])
        urls.append(row[1])
        dates.append(row[2])
        pubs.append(row[3])
        content.append(row[4])

filtered_dates = list(filter(None, dates))
formatted_dates = []

from dateutil import parser
for i in filtered_dates:
    d = parser.parse(i)
    formatted_dates.append(d.strftime("%Y-%m-%d %H:%M:%S"))

# atom expects a 2-dimensional array, so reshape to (n_articles, 1)
# X = np.array(content).reshape(-1, 1)
# atom = ATOMClassifier(X, test_size=0.2, verbose=2)

# atom.textclean()
# atom.tokenize()
# atom.textnormalize(stopwords="english", lemmatize=True)
# atom.tokenize(bigram_freq=200)
# atom.vectorize(strategy="tfidf")

# atom.plot_wordcloud()
# atom.plot_ngrams(ngram=2)

# print(atom.dataset)
# print(atom.available_models())

# atom.run(models="RF", metric="f1_weighted")
# atom.evaluate()
# atom.plot_confusion_matrix()
# atom.decision_plot(index=0, target=atom.predict(0), show=10)
# atom.beeswarm_plot(target=0, show=15)