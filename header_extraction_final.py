import smtplib
import time
import imaplib
import email
from maillogin import *
import sys

def extract_header():
	oldstdout = sys.stdout
	f = open("header.out","w")
	sys.stdout = f
	mail = imaplib.IMAP4_SSL(SMTP_SERVER)
	mail.login(FROM_EMAIL,FROM_PWD)
	mail.select('inbox')
	result, data = mail.uid('search', None, 'ALL')
	uids = data[0].split()
	for uid in reversed(uids):
		result, data = mail.uid('fetch',uid,'(RFC822.HEADER)')
		d = data[0][1].splitlines()
		for temp in d:
			print(temp)
		break
	f.close()
	sys.stdout = oldstdout