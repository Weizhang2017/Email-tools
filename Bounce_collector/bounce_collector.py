from SMTPEmail import IMAP
from Bounce_classifier.bounce_classifier import Bounce_classifier
from mongoengine import *
import datetime
import requests

class EmailServer:

	def __init__(self,ip_addr,account,password):
		self.IMAP_client = IMAP(
						IMAP_server=ip_addr,
						IMAP_account=account,
						IMAP_password=password
			)

	def retrieve_bounce_smtp(self,mail_box):
		#this task is for cron job to retrieve bounces from email server
		try:

			for msg in self.IMAP_client.retrieve_msg(delete=False,mailbox_name=mail_box, msg_id='all'):
				if isinstance(msg[0], bytes):
					message_format = msg[0].decode("utf-8", "ignore")
				else:
					message_format = str(msg[0])
				if isinstance(msg[1], bytes):
					message = msg[1].decode("utf-8", "ignore")
				else:
					message = str(msg[1])
				yield message
		except ValueError as e:
			print(str(e))

	@staticmethod
	def retrieve_bounce_sendgrid(api_key):
		url = 'https://api.sendgrid.com/v3/suppression/bounces'
		res = requests.get(url, headers={'Authorization': 'Bearer {}'.format(api_key), 'accept': "application/json"})
		print(res.content)

class Message:
	def __init__(self, message):
		self.message = message

	def classify(self):
		bc = Bounce_classifier(self.message)
		catalogue, key_word = bc.no_diagonostic_code()
		return catalogue, key_word
