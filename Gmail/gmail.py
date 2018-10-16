import sys
import imaplib
import email
import email.header
import re
logging.basicConfig(level=logging.INFO)

class Retrive_gmail(object):


	def __init__(self, account, password):
		self.account = account
		self.con_email = imaplib.IMAP4_SSL('imap.gmail.com')
		try:
			rv, data = self.con_email.login(account, password)
			rv, mailbox_list = self.con_email.list()
			for ind, item in enumerate(mailbox_list):
				item = re.search(r'\"[\w\-\[\]\.\/\s\@\(\)]+\"$', item.decode()).group()
				print('%s. %s' %(ind, item))
			choice = input('Please select the folder to retrieve emails: ')
			self.mailbox = re.search(r'\"[\w\-\[\]\.\/\s\@\(\)]+\"$', mailbox_list[int(choice)].decode()).group()#.decode().split()[-1]
			rv, totol_email = self.con_email.select(self.mailbox)
			rv, email_ids = self.con_email.search(None, 'ALL')
			email_list = email_ids[0].split()
			self.store_mail(email_list)
		except Exception as e:
			logging.error('login failed, %s' % e)
			sys.exit(1)

	def store_mail(self, email_list):
		con_mongodb = MongoClient('localhost', 27017).email_classfication.train
		counter = 0
		for mail_id in email_list:
			try:
				rv, data = self.con_email.fetch(mail_id, '(RFC822)')
				msg = email.message_from_bytes(data[0][1])
				msg_dict = dict(msg)
				msg_dict['from_account'] = self.account
				msg_dict['label'] = self.mailbox
				for part in msg.walk():
					body = part.get_payload()
					if isinstance(body, str):
						msg_dict['body'] = body
						break
				if isinstance(msg_dict['Subject'], email.header.Header):
					msg_dict['Subject'] = str(email.header.make_header(email.header.decode_header(msg_dict['Subject'])))
				con_mongodb.insert_one(msg_dict)
				logging.info('inserted, %s' % counter)
			except Exception as e:
				logging.error('storing email error: %s' % e)
				try:
					if isinstance(msg_dict.get('Subject'), email.header.Header):
						msg_dict['Subject'] = str(email.header.make_header(email.header.decode_header(msg_dict['Subject'])))
					if isinstance(msg_dict.get('From'), email.header.Header):
						msg_dict['From'] = str(email.header.make_header(email.header.decode_header(msg_dict['From'])))
					if msg_dict.get('X-smtpout4.coopanet.com-MailScanner-ID'):
						msg_dict.pop('X-smtpout4.coopanet.com-MailScanner-ID')
					if msg_dict.get('X-smtpout4.coopanet.com-MailScanner'):
						msg_dict.pop('X-smtpout4.coopanet.com-MailScanner')
					con_mongodb.insert_one(msg_dict)
				except Exception as e:
					logging.error('storing email error again: %s' % e)
					import pdb;pdb.set_trace()
			finally:
				counter += 1

	def test_store_mail(self, email_list):
		counter = 0
		for mail_id in email_list:
			rv, data = self.con_email.fetch(mail_id, '(RFC822)')
			msg = email.message_from_bytes(data[0][1])
			for part in (msg.walk()):
				# logging.info('%s \n %s' % ('='*128,part))
				print(part.get_payload())
				logging.info('*'*128)
				import pdb; pdb.set_trace()