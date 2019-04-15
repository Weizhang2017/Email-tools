from bounce_collector import *
'''
def test_email_server():
	es = EmailServer('doomer.site', 'marketing@doomer.site', '123welcome123')
	import pdb;pdb.set_trace()
	for message in es.retrieve_bounce_smtp('inbox'):
		print(message)
	print('done')
'''
def test_classify():
	es = EmailServer('doomer.site', 'marketing@doomer.site', '123welcome123')
	import pdb;pdb.set_trace()
	for message in es.retrieve_bounce_smtp('inbox'):
		msg = Message(message)
		print(msg.classify())