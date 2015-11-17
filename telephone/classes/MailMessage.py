from email.mime.text import MIMEText
import os
from smtplib import SMTP_SSL
from django.template import Context
from django.template.loader import get_template
from telephone import settings
from telephone.service_app.services.LogService import LogService, Code


class MailMessage():
	def __init__(self, sender, subject, template, context, *destination):
		self.__text_subtype = 'html'
		self.__sender = sender
		self.__destination = [d for d in destination]
		self.__template = template
		self.__subject = subject
		self.__template_context = context

	@property
	def sender(self):
		"""
		Getter of __sender
		:return: sender value
		"""
		return self.__sender

	@property
	def destination(self):
		"""
		Getter of __destination
		:return: destination value
		"""
		return self.__destination

	@property
	def content(self):
		"""
		Getter of __content
		:return: content value
		"""
		return get_template(self.__template).render(Context(self.__template_context))

	@property
	def subject(self):
		"""
		Getter of __subject
		:return: subject value
		"""
		return self.__subject

	@property
	def text_subtype(self):
		"""
		Getter of __text_subtype
		:return: text_subtype value
		"""
		return self.__text_subtype

	def get_message(self):
		"""
		Returns MIMEText instance of message content
		:return: MIMEText instance
		"""
		msg = MIMEText(self.content.encode('UTF-8'), self.__text_subtype)
		msg['Subject'] = self.__subject
		msg['From'] = self.__sender
		return msg

	def send(self, smtp='smtp.yandex.com', username='info@web-tel.ru', password='Info112911'):
		"""
		Send email message
		:param smtp: server to send message
		:param username: server to send message
		:param password: server to send message
		:return:
		"""
		try:
			connection = SMTP_SSL(smtp)
			connection.set_debuglevel(False)
			connection.login(username, password)
			connection.sendmail(self.__sender, self.__destination, self.get_message().as_string())
			connection.close()
			return True
		except Exception as e:
			logger = LogService()
			logger.error(Code.EMAIL_SEND_ERR, message=str(e))
			return False