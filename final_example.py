import sys
from keywordextraction import *
from nltk.corpus import stopwords
from google import search
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
from urllib.parse import urlparse
import socket 
from age_of_domain_final import *
from pprint import pprint
from header_extraction_final import *
from url_extraction_final import *
from body_extraction_final import *
from maillogin import *
from google_search_using_api_final import *
import tldextract
from pprint import pprint
#from dns_resolver import *
#from ipaddress_extraction_final import *
from other_features_of_url import *
def extract_domain(url):
	try:
		key1 = urlparse(url)
		key1 = '{uri.scheme}://{uri.netloc}/'.format(uri=key1)
		return key1
	except:
		return -1

stoplist = stopwords.words('english')
def check(url):
	global blacklist
	print(url)
	key1 = extract_domain(url)
	if(key1==-1):
		print("\033[1;4;91mNOT FOUND!!\033[0m")
		return -1

	if(key1 == 'https://google.com'):
		print('\033[1;4;92mIt is Google\033[0m')
		return 1
	if(key1 == 'https://gmail.com'):
		print('\033[1;4;92mIt is Gmail\033[0m')
		return 1
	print("key1 "+key1)
	if(str(key1) in blacklist):
		print("\033[1;4;91murl in blacklist\033[0m")
		return -1
	if(key1==-1):
		print("\033[1;4;91mNOT FOUND\033[0m")
		return -1
	try:
		html = urlopen(url).read()
	except ValueError:
		print("\033[1;4;91moops!!\033[0m")
		return
	soup = BeautifulSoup(html)
	for script in soup(["script","style"]):
		script.extract()
	
	text = soup.get_text()
	lines = (line.strip() for line in text.splitlines())
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	text = '\n'.join(chunk for chunk in chunks if chunk)
	content = text

	preload=1
	classifier_type = 'logistic'
	keyword_classifier = get_keywordclassifier(preload,classifier_type)['model']
	top_k = 20
	flag = 0
	keywords = extract_keywords(text,keyword_classifier,top_k,preload)

	for key in keywords:
		if key not in stoplist:
			links = google_search(key,my_api_key, my_cse_id, num=10)
			for url2 in links:
				key2 = extract_domain(url2)
				print(key1 + " " + key2)
				if(key1==key2):
					flag=1
					break
			if flag==1:
				print("\033[1;4;92murl found on google search\033[0m")
				return 1	
	print(url+ ' ' +str(flag))

	age=age_of_domain(key1)
	print("\033[1;4;92mage: "+str(age)+"\033[0m")
	if(age >= 2):
		print("\033[1;4;92mAge of domain is "+str(age)+"\033[0m")
		return 1
	print("\033[1;4;91mURL not Found\033[0m")
	return -1


if __name__ == "__main__":
	with open("/home/sagarwal/phishing detection/blacklistedwebsites.txt") as f:
		blacklist = f.read().splitlines()
	#extract_body()
	urls = extract_urls()
	total_urls = 0
	neg_res = 0
	suspicious_url = 0
	for url in urls:
		print(url)
		ans = check(url)
		if(ans==1):
			total_urls = total_urls + 1
		else:
			et = extract_domain(url)
			if et not in blacklist:
				factor1 = length(url)
				factor2 = url_contains_ipaddress(url)
				factor3 = url_contains_symbol(url)
				factor4 = url_contains_symbolii(url)
				factor5 = num_domainsandsubdomains(url)
				factor6 = url_redirection(url)
				if(factor1==1 and factor2==1 and factor3==1 and factor4==1 and factor5==1 and factor6==1):
					total_urls = total_urls + 1
				elif(factor1==-1 or factor2==-1 or factor3==-1 and factor4==-1 or factor5==-1 or factor6==-1):
					neg_res = neg_res + 1
				else:
					suspicious_url = suspicious_url+1
			else:
				neg_res = neg_res + 1		
	print("\033[1;4;92mValid URLS: "+str(total_urls)+'\033[0m')
	print("\033[1;4;91mInvalid URLS: "+str(neg_res)+'\033[0m')
	if(neg_res == 0 and suspicious_url==0):
		print("********************\033[1;4;92mEmail is LEGITIMATE\033[0m********************")
	elif(neg_res == 0 and suspicious_url != 0):
		print("********************\033[1;4;94mEmail is SUSPICIOUS\033[0m********************")
	else:
		print("********************\033[1;4;91mEmail is PHISHY\033[0m********************")
