import regexforurl_final
import re
from pprint import pprint
import urllib
from urllib.request import urlopen
from urllib.parse import urlparse

def extract_domain(url):

	try:
		key1 = urlparse(url)
		key1 = '{uri.scheme}://{uri.netloc}/'.format(uri=key1)
		return key1
	except:
		return -1

def extract_urls():
	with open("body.out","r") as f:
		urls = set()
		ex = f.read()
		urls.update(re.findall(regexforurl_final.WEB_URL_REGEX,ex))
		furl = set()
		for url in urls:
			if(url[:8]!='https://'):
				continue
			key = extract_domain(url)
			if key!=-1:
				furl.update([key])
		return furl
