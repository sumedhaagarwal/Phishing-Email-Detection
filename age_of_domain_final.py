import whois
from dateutil import relativedelta
import datetime
import sys
import glob
import urllib
from urllib.request import urlopen
from urllib.parse import urlparse

def age_of_domain(domain):
	try:
		whois_info = whois.whois(domain.lower())
		if whois_info.creation_date:
			current_date = datetime.datetime.now()
			try:
				created_on = whois_info.creation_date[0]
				diff = relativedelta.relativedelta(current_date,created_on)
			except:
				return -1
			return (diff.years)
		else:
			return -1
	except:
		return -2;