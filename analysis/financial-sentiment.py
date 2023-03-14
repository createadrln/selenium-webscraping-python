from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import string
import re
import pandas as pd
import nltk

# Function to print sentiment of sentences
def sentiment_scores(sentence):

    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)

    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")

    print("Sentence Overall Rated As", end=" ")

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        print("Positive")

    elif sentiment_dict['compound'] <= -0.05:
        print("Negative")

    else:
        print("Neutral")

def clean_text(article):
    clean1 = re.sub(r'[' + string.punctuation + '’—”' + ']', "",
                    "".join(article).lower())
    return re.sub(r'\W+', ' ', clean1)

f1 = pd.read_csv('data-files/financial-blogs-data/afford-anything.csv')
all_articles = pd.read_csv('data-files/financial-blogs-data/combined.csv')
all_articles['tokenized'] = all_articles['content'].map(lambda x: clean_text(x))

# TODO Need to join all the sentences together in the files

article_sent_text = nltk.sent_tokenize(f1['content'][0])
print(f1['content'][0])

# article_sentences = []

# for article_content in f1['content']:
    # article_sent_text = nltk.sent_tokenize(article_content)
    # article_sentences.append(article_sent_text)

# print(article_sentences)

# Driver code
# if __name__ == "__main__":


    # function calling
    # sentiment_scores(f1['tokenized'])

    # print("\n2nd Statement :")
    # sentence = "study is going on as usual"
    # sentiment_scores(sentence)

    # print("\n3rd Statement :")
    # sentence = "I am very sad today."
    # sentiment_scores(sentence)
