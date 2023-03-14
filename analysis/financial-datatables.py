import pandas as pd
import re
import string
import numpy as np
from collections import Counter

import nltk
from nltk.corpus import stopwords

def clean_text(article):
    clean1 = re.sub(r'[' + string.punctuation + '’—”' + ']', "",
                    "".join(article).lower())
    return re.sub(r'\W+', ' ', clean1)

articles = pd.read_csv('data-files/financial-blogs-data/combined.csv')
articles['tokenized'] = articles['content'].map(lambda x: clean_text(x))
articles['num_wds'] = articles['tokenized'].apply(lambda x: len(x.split()))
# articles = articles[articles['num_wds'] > 0]
# articles['uniq_wds'] = articles['tokenized'].str.split().apply(     
#     lambda x: len(set(x)))

#-------

# Let's look at the distribution of the number of words in the articles in a histogram.

import matplotlib.pyplot as plt

ax = articles['uniq_wds'].plot(kind='hist', bins=50, fontsize=14, figsize=(12,10))
ax.set_title('Unique Words Per Article\n', fontsize=20)
ax.set_ylabel('Frequency', fontsize=18)
ax.set_xlabel('Number of Unique Words', fontsize=18)

# plt.show()

#-------

# Ok, so we have a lot of articles with very few unique words. Let's look at the most common words and phrases in the corpus.

wd_counts = Counter()
wd_counts_bigrams = Counter()
wd_counts_trigrams = Counter()

for i, row in articles.iterrows():
    wd_counts.update(row['tokenized'].split())
    wd_counts_bigrams.update(list(nltk.bigrams(row['tokenized'].split())))
    wd_counts_trigrams.update(list(nltk.trigrams(row['tokenized'].split())))

english_stops = stopwords.words('english')

for sw in english_stops:
    del wd_counts[sw]

clean_bigrams = []
for gram, count in wd_counts_bigrams.most_common(50):
    if not any (stop in gram for stop in english_stops):
        clean_bigrams.append((gram, count))

# How can we make this return better results? trigram_stops does not work yet.

clean_trigrams = []
trigram_stops = [('one', 'of', 'the')]
for gram, count in wd_counts_trigrams.most_common(50):
    if not any (stop in gram for stop in trigram_stops):
        clean_trigrams.append((gram, count))

# print(clean_bigrams)
# print(clean_trigrams)

#-------

# We can apply some specific financial terms to the corpus to see if we can find any articles that are more likely to be about finance.

def find_financial_wds(content, cc_wds=['make money', 'credit', 'financial institution', 'financial advisor', 'financial independence', 'financial future' 'market', 'credit card', 'pay', 'credit line', 'credit management']
):
    found = False
    for w in cc_wds:
        if w in content:
            found = True
            break

    if not found:
        disj = re.compile(r'(chang\w+\W+(?:\w+\W+){1,5}?climate) | (climate\W+(?:\w+\W+){1,5}?chang)')
        if disj.match(content):
            found = True
    return found
    
articles['financial_wds'] = articles['tokenized'].apply(find_financial_wds)

# print(articles['financial_wds'].head())
# print(articles['financial_wds'].sum() / len(articles))

#-------

# More word stats

word_counts = []

# I think we want to test this with the n grams?
word_counts['most_common'] = wd_counts.most_common(20)

mcw = word_counts['most_common'].plot(kind='hist', bins=50, fontsize=14, figsize=(12,10))
mcw.set_title('Most Common Words\n', fontsize=20)
mcw.set_ylabel('Frequency', fontsize=18)
mcw.set_xlabel('Number of Unique Words', fontsize=18)

# plt.show()
