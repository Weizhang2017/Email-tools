import re
import logging

logging.basicConfig(filename='error.log', level=logging.ERROR) 

class Bounce_classifier(object):
	'''Classify bounce messages using regex'''
	def __init__(self, email_text):
		
		self.email_text = email_text.lower()

	def recipient_email(self):
		try:
			rcpt = re.search('final-recipient: (rfc822;|)(.*?)\n', self.email_text).group(2)
		except Exception as e:
			rcpt = 'Not found'
			return rcpt
		return rcpt

	def diagonostic_code(self):
		try:
			dia_code = re.search('diagnostic-code: (.*?)\n', self.email_text).group(1)
		except Exception as e:
			dia_code = None
			classification = 'unclassified'
			return dia_code, classification

		if re.search('njabl', dia_code):
			classification = 'blacklist'
		elif re.search('message.*(size\sexceed|too\slarge)', dia_code):
			classification = 'msgsize'
		elif re.search('temporar.*(problem|reject)|insufficient.*resource|out\sof\ssequence|mail.*loop.*\
			.*detected|(service|transport)\sunavailable', dia_code):
			classification = 'temperr'
		elif re.search('(invalid|disabled|deactivated|malformed|norelay|inactiv(e|ity)|\
						no.*(account|such|mailbox|address)|\
						(address(ee?)|user).*(not\slisted|failed|doesn|unknown)|\
						not.*(exist|found|.*valid|our\scustomer)|\
						unknown(.*?)\s(user|alias|recipient)|\
						alias.*valid|\
						address\slookup.*fail|\
						format.*address|\
						unrouteable\saddress|\
						(recipient|address).*\s(rejected|no\slonger)|\
						none\s.*servers.*respond|\
						no\s(route\sto\shost|valid|recipient)|\
						hop\scount\sexceeded|\
						RP:RDN.*xrnet|\
						too\smany\shops|\
						list\sof\sallowed\srcpthosts|\
						user.*(reject|suspend)|\
						doesn.*\shandle\smail\sfor|\
						(user|recipient).*(not|only|unknown)|\
						unknow\suser\
						(access|relay).*\sdenied|\
						MX\spoints\sto|\
						refused\sdue\sto\srecipient|\
						(account|mailbox|address|recipient).*\
						(reserved|suspended|unavailable|not)|\
						loops\sback\sto\smyself)', dia_code):
			classification = 'deadrcpt'
		elif re.search('(\s550\s5\.7\.1|\
						too\s(many|fast|much)|slow\sdown|throttl(e|ing)|\
						to\sabuse|excessive|bl(a|o)cklist|\
						(junk|intrusion)|\
						listed\sat|\
						client.*not\sauthenticated|\
						administrative.*prohibit|\
						connection\srefused|\
						connection.*(timed\sout|limit)|\
						refused.*(mxrate|to\stalk)|\
						can.*connect\sto\s.*psmtp|\
						reject.*(content|policy)|\
						not\saccept.*mail|\
						message.*re(fused|ject)|\
						transaction\sfailed.*psmtp|\
						sorbs|rbl|spam|spamcop|block|den(y|ied)|\
						unsolicited|\
						not\sauthorized\sfrom\sthis\sip|\
						reject\smail\sfrom|try\sagain\slater)|\
						|too\s(much|many)', dia_code):
			classification = 'blocked'
		elif re.search('(overquota|over\squota|quota\sexceed|\
						exceeded.*storage|\
						(size|storage|mailbox).*(full|exceed)|\
						full\s.*mailbox)', dia_code):
			classification = 'fullbox'
		elif re.search('message.*delayed', dia_code):
			classification = 'delayed'
		else:
			classification = 'unclassified'

		return dia_code, classification

	def no_diagonostic_code(self):

		# BEGIN: message autoreply 

		if re.search('X-Autoreply:\s*yes', self.email_text):
			classification = "autoreply"
			
		elif re.search('Subject:.*(out\s+of.*office|auto.*re(ply|spon))', self.email_text):
			classification = "autoreply"
		elif re.search('\s\(aol;\saway\)', self.email_text):
			classification = "autoreply"
		elif re.search('auto-submitted:\s*auto-replied', self.email_text):
			classification = "autoreply"

		# BEGIN: message delayed notification
		elif re.search('(Action:\s*delayed|Will-Retry-Until)', self.email_text):
		  classification = "delayed"
		elif re.search('Subject:.*delayed\smail', self.email_text):
		  classification = "delayed"
		elif re.search('Subject:.*delivery.*status.*delay', self.email_text):
		  classification = "delayed"
		elif re.search('delivery\sto.*has\sbeen\sdelayed', self.email_text):
		  classification = "delayed"

		# BEGIN: dead recipient address
		elif re.search('this\suser\sdoesn\'t\shave\sa\s.*\saccount', self.email_text):
		  classification = "deadrcpt"
		elif re.search('user.*doesn.*mail.*your.*address', self.email_text):
		  classification = "deadrcpt"
		elif re.search('in\smy\scontrol.*locals', self.email_text):
		  classification = "deadrcpt"
		elif re.search('invalid.*mailbox', self.email_text):
		  classification = "deadrcpt"
		elif re.search('user\sunknown|unknown\suser', self.email_text):
		  classification = "deadrcpt"
		elif re.search('message.*not\sbe\sdelivered', self.email_text):
		  classification = "deadrcpt"
		elif re.search('address\swas\snot\sfound', self.email_text):
		  classification = "deadrcpt"
		elif re.search('protected.*bluebottle', self.email_text):
		  classification = "deadrcpt"
		elif re.search('hop\scount\sexceeded', self.email_text):
		  classification = "deadrcpt"
		elif re.search('delivery\sto.*(failed|aborted\safter)', self.email_text):
		  classification = "deadrcpt"

		# BEGIN: full mailbox
		elif re.search('(size|(in|mail)box).*(full|size|exceed|many\smessages|much\sdata)', self.email_text):
		  classification = "fullbox"
		elif re.search('quota.*exceed', self.email_text):
		  classification = "fullbox"

		# BEGIN: rbl'policy block
		elif re.search('5\.7\.1.*(reject|spam)', self.email_text):
		  classification = "blocked"
		elif re.search('protected.*reflexion', self.email_text):
		  classification = "blocked"
		elif re.search('said:\s.*(spam|rbl|blocked|blacklist|abuse)', self.email_text):
		  classification = "blocked"
		elif re.search('reputation', self.email_text):
		  classification = "blocked"
		# BEGIN: temporary error
		elif re.search('open\smailbox\sfor\s.*\stemporary\serror', self.email_text):
		  classification = "tmperr"
		elif re.search('subject.*mail\ssystem\serror', self.email_text):
		  classification = "tmperr"

		# BEGIN: unclassified catchall
		else:
		  classification = "unclassified"
		return classification
