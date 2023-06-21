# Text cleaning

import string
import re

def clean_text(text):
    # Remove punctuation
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    # Remove digits
    text = re.sub('\d+', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove whitespace
    text = text.strip()
    
    return text

def clean_date_text(text):
    # Remove punctuation
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    
    return text