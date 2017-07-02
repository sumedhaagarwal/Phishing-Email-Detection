import re
import sys

def extract_ipaddress():
	with open("header.out","r") as f:
		ex = f.read()
		urls=set()
		urls.update(re.findall (r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',ex))
		return urls

#print(extract_ipaddress())