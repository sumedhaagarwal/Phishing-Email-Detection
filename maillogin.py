import getpass

FROM_EMAIL = input("Enter email address: ")
FROM_PWD = getpass.getpass()
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993