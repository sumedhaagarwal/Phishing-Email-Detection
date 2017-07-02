import re
import string
import nltk
from nltk.tag import StanfordNERTagger
from nltk.collocations import *
from gensim import corpora, models, similarities
from collections import defaultdict
import wikiwords
import numpy as np


def remove_punctuation(text):
	exclude = set(string.punctuation)
	return ''.join([ch for ch in text if ch not in exclude])

def get_namedentities(text):
	st = StanfordNERTagger('/home/sagarwal/phishing detection/keyword_extraction/dataset/english.conll.4class.caseless.distsim.crf.ser.gz','/home/sagarwal/phishing detection/keyword_extraction/dataset/stanford-ner.jar')
	ner_tagged = st.tag(text.lower().split())
	named_entities = []
	if len(ner_tagged) > 0:
		for n in ner_tagged:
			if n[1]!='0':
				named_entities.append(remove_punctuation(n[0]))
	named_entities = [n for n in named_entities if n]
	return named_entities

def get_nounphrases(text):
	grammar = r""" 
	    NBAR:
	        {<NN.*|JJ>*<NN.*>}  
	    NP:
	        {<NBAR>}
	        {<NBAR><IN><NBAR>} 
	"""   
	chunker = nltk.RegexpParser(grammar)
	sentences = nltk.sent_tokenize(text.lower())
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	noun_phrases = []
	for sent in sentences:
		tree = chunker.parse(sent)
		for subtree in tree.subtrees():
			if subtree.label() == 'NP':
				noun_phrases.extend([w[0] for w in subtree.leaves()])
	noun_phrases = [remove_punctuation(nphrase) for nphrase in noun_phrases]
	noun_phrases = [n for n in noun_phrases if n]
	return noun_phrases

def get_trigrams(text,num_trigrams):
	trigram_measures = nltk.collocations.TrigramAssocMeasures()
	finder = TrigramCollocationFinder.from_words(text.lower().split())
	finder.apply_freq_filter(1)
	top_ngrams = finder.nbest(trigram_measures.pmi,num_trigrams)
	ngrams = []
	for ng in top_ngrams:
		ngrams.extend(list(ng))
	ngrams = [remove_punctuation(n) for n in list(set(ngrams))]
	ngrams = [n for n in ngrams if n]
	return ngrams

def get_binaryfeature(words,selected_words):
	feature = map(lambda x: 1 if x else 0, [(w in selected_words) for w in words])
	feature = list(feature)
	return feature

def get_termfrequency(text,candidate_keywords):
	words = [remove_punctuation(w) for w in text.lower().split()]
	return [sum([1 for w in words if w==c])/float(len(words)) for c in candidate_keywords]

def get_tfidf(candidate_keywords,corpus_entry,dictionary):
	weights = []
	if corpus_entry:
		for candidate in candidate_keywords:
			if candidate in dictionary.token2id:
				tfidf_score = [w[1] for w in corpus_entry if w[0]==dictionary.token2id[candidate]]
				if len(tfidf_score)>0:
					weights.append(tfidf_score[0])
				else:
					weights.append(0)
			else:
				weights.append(0)
	else:
		weights = [0]*len(candidate_keywords)

	return weights

def get_length(candidate_keywords):
	max_chars = 50
	return [len(c)/float(max_chars) for c in candidate_keywords]

def get_position(text,candidate_keywords):
	words = [remove_punctuation(w) for w in text.lower().split()]
	position = []
	for candidate in candidate_keywords:
		occurences = [pos for pos,w in enumerate(words) if w == candidate]
		if len(occurences)>0:
			position.append(occurences[0]/float(len(words)))
		else:
			position.append(0)
	return position

def get_spread(text,candidate_keywords):
	words = [remove_punctuation(w) for w in text.lower().split()]
	spread = []
	for candidate in candidate_keywords:
		occurences = [pos for pos,w in enumerate(words) if w == candidate]
		if len(occurences)>0:
			spread.append((occurences[-1]-occurences[0])/float(len(words)))
		else:
			spread.append(0)
	return spread

def get_capitalized(text,candidate_keywords):
	words_original = [remove_punctuation(w) for w in text.split()]
	words_lower = [remove_punctuation(w) for w in text.lower().split()]
	caps = []
	for candidate in candidate_keywords:
		occurences = [pos for pos,w in enumerate(words_lower) if w == candidate]
		if len(occurences)>0:
			any_caps = sum([1 for o in occurences if words_original[o]!=words_lower[o]])
			if any_caps>0:
				caps.append(1)
			else:
				caps.append(0)
		else:
			caps.append(0)
	return caps

def get_wikifrequencies(candidate_keywords):
	max_frequency = wikiwords.freq('the')
	return [wikiwords.freq(w)/float(max_frequency) for w in candidate_keywords]

def extract_features(text,candidate_keywords,corpus_entry,dictionary):
	num_features = 10
	num_trigrams = 5
	named_entities = get_namedentities(text)
	noun_phrases = get_nounphrases(text)
	top_trigrams = get_trigrams(text,num_trigrams)
	ne_feature = np.array(get_binaryfeature(candidate_keywords,named_entities))
	np_feature = np.array(get_binaryfeature(candidate_keywords,noun_phrases))
	ng_feature = np.array(get_binaryfeature(candidate_keywords,top_trigrams))
	tf_feature = np.array(get_termfrequency(text,candidate_keywords))
	tfidf_feature = np.array(get_tfidf(candidate_keywords,corpus_entry,dictionary))
	length_feature = np.array(get_length(candidate_keywords))
	position_feature = np.array(get_position(text,candidate_keywords))
	spread_feature = np.array(get_spread(text,candidate_keywords))
	caps_feature = np.array(get_capitalized(text,candidate_keywords))
	wiki_feature = np.array(get_wikifrequencies(candidate_keywords))
	features = np.zeros((len(candidate_keywords),num_features))
	features[:,0] = ne_feature
	features[:,1] = np_feature
	features[:,2] = ng_feature
	features[:,3] = tf_feature
	features[:,4] = tfidf_feature
	features[:,5] = length_feature
	features[:,6] = position_feature
	features[:,7] = spread_feature
	features[:,8] = caps_feature
	features[:,9] = wiki_feature
	feature_names = ['Named Entity','Noun Phrase','N-gram','Term Freq','TF-IDF','Term Length','First Occurence','Spread','Capitalized','Wikipedia frequency']
	return {'features' : features, 'names' : feature_names}
