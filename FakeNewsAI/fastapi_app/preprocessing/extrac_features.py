import numpy as np
import pandas as pd
import textstat 
import re
from collections import Counter


#######################################################
#basic feature
#######################################################

def avg_word_length_long_words(text):
    words = text.split()
    long_words = [w for w in words if len(w) >= 4]
    if not long_words:  # avoid division by zero
        return 0
    return sum(len(w) for w in long_words) / len(long_words)

def num_unique_words(text):
    return len(set(text.split()))


def avg_word_length(text):
    words = text.split()
    return np.mean([len(w) for w in words]) if words else 0


def punctuation_count(text):
    return len(re.findall(r'[^\w\s]', text))


def exclamation_count(text):
    return text.count('!')

def question_count(text):
    return text.count('?')

def num_uppercase_words(text):
    return sum(1 for w in text.split() if w.isupper())


def title_word_overlap_ratio(text, title):
    if not title:
        return 0
    title_words = set(title.lower().split())
    text_words = set(text.lower().split())
    if len(title_words) == 0:
        return 0
    return len(title_words & text_words) / len(title_words)


def contains_hyperlink(text):
    return int('http' in text or 'www' in text)


def avg_sentences_length(text):
    # Split by '.', filter out empty sentences
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    if not sentences:
        return 0
    # Count words in each sentence
    sentences_length = [len(s.split()) for s in sentences]
    return np.mean(sentences_length)

def num_word(text):
    return len(text.split())


def num_sentences(text):
    # Split on ., !, ? followed by a space or end of string
    sentences = re.split(r'[.!?]+(?:\s|$)', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences)

def vocabulary_richness(text):
    words=[word for word in text.split()]
    if(len(words)==0):
        return 0
    res=len(set(words)) / len(words)
    return res


def most_used_word_count(text):
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0
    word_counts = Counter(words)
    return word_counts.most_common(1)[0][1]  # just the count






##########################################################################
#language processing feature
##########################################################################

def readablitity(text):
    score=textstat.flesch_reading_ease(text)
    return score


def smog_index(text):
    index=textstat.smog_index(text)
    return index

def difficalt_word(text):
    difficality=textstat.difficult_words(text)
    return difficality


def extract_features(text, title):
    return {
        'num_unique_words': num_unique_words(text),
        'avg_word_length': avg_word_length(text),
        'punctuation_count': punctuation_count(text),
        'exclamation_count': exclamation_count(text),
        'question_count': question_count(text),
        'num_uppercase_words': num_uppercase_words(text),
        'title_word_overlap_ratio': title_word_overlap_ratio(text, title),
        'contains_hyperlink': contains_hyperlink(text),
        'avg_len_4plus': avg_word_length_long_words(text),
        'avg_len_sentences': avg_sentences_length(text),
        'number_word': num_word(text),
        'num_sentences': num_sentences(text),
        'vocabulary_richness': vocabulary_richness(text),
        'most_used_word':most_used_word_count(text),
        'readablility_text':readablitity(text),
        'smog':smog_index(text),
        'difficalt_word':difficalt_word(text)
    }