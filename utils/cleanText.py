# Text cleaning

import string
import re

def clean_text(text):
    text = clean_text_remove_punct(text)
    
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

def clean_text_remove_punct(text):
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    return text

def text_remove_brackets_and_line_breaks(text):
    cleanText = re.sub(r'\]|\[|', '', text)
    cleanText = re.sub(r'\\n', ' ', cleanText)
    return cleanText
