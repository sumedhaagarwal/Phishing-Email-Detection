import os
import re
import random
import numpy as np 
import pickle
import string
import nltk
from nltk.corpus import stopwords
stoplist = stopwords.words('english')
from gensim import corpora, models, similarities
from collections import defaultdict
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from features import *

def get_keywordclassifier(preload,classifier_type):
	train_XY = pickle.load(open('saved/trainXY_crowd500.pkl','rb'),encoding='latin1')
	test_XY = pickle.load(open('saved/testXY_crowd500.pkl','rb'),encoding='latin1') 
	model = pickle.load(open('saved/logisticregression_crowd500.pkl','rb'),encoding='latin1') 
	return {'model': model, 'train_XY':train_XY, 'test_XY':test_XY}

def generate_candidates(text):
	num_trigrams = 5
	named_entities = get_namedentities(text)
	noun_phrases = get_nounphrases(text)
	top_trigrams = get_trigrams(text,num_trigrams)
	return list(set.union(set(named_entities),set(noun_phrases),set(top_trigrams)))

def extract_keywords(text,keyword_classifier,top_k,preload):
	preprocessing = pickle.load(open('saved/tfidf_preprocessing.pkl','rb'),encoding='latin1')
	dictionary = preprocessing['dictionary']
	tfidf = preprocessing['tfidf_model']
	
	text_processed = [remove_punctuation(word) for word in text.lower().split() if word not in stoplist]
	corpus = [dictionary.doc2bow(text_processed)]
	corpus_entry = tfidf[corpus][0]

	candidate_keywords = generate_candidates(text)
	if len(candidate_keywords) < top_k:
		candidate_keywords = text_processed   
	feature_set = extract_features(text,candidate_keywords,corpus_entry,dictionary)
	predicted_prob = keyword_classifier.predict_proba(feature_set['features'])
	this_column = np.where(keyword_classifier.classes_==1)[0][0]
	sorted_indices = [i[0] for i in sorted(enumerate(predicted_prob[:,this_column]),key = lambda x:x[1],reverse = True)]
	chosen_keywords = [candidate_keywords[j] for j in sorted_indices[:top_k]]    
	return chosen_keywords