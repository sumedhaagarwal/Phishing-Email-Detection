import requests
import re
import sys
import tldextract

def length(url):
	length_of_url = len(url)
	if(length_of_url<=54):
		return 1
	elif(length_of_url>54 and length_of_url<74):
		return 0
	else:
		return -1

def url_contains_ipaddress(url):
	if len(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url))!=0:
		return -1
	return 1

def url_contains_symbol(url):
	if url.find('@') is not -1:
		return -1
	return 1

def url_contains_symbolii(url):
	try:
		if ((tldextract.extract(url)).domain).find('-') is not -1:
			return -1
	except:
		return -1
	return 1

def num_domainsandsubdomains(url):
	if(url.count('.') < 3):
		return 1
	elif(url.count('.')==3):
		return 0
	else:
		return -1

def url_redirection(url):
	try:
		try:
			response = requests.get(url)
		except:
			return -1
		if response.history:
			return -1
		else:
			return 1
	except:
		url = 'https://' + url
		try:
			response = requests.get(url)
		except:
			return -1
		if response.history:
			return -1
		else:
			return 1