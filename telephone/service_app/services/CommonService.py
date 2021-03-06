# coding=utf-8
from base64 import b64encode
import calendar
import hashlib
import hmac
import os
import string
import datetime
import urllib
import uuid
import math

from django.utils import crypto
from pydub import AudioSegment

from telephone import settings
from telephone.classes.File import File
from telephone.service_app.services.LogService import LogService, Code


class Constants():
	def __init__(self):
		pass

	CUR_DATE_DAY_START_STR = datetime.datetime.now().strftime(settings.DATETIME_FORMAT_START)
	CUR_DATE_DAY_END_STR = datetime.datetime.now().strftime(settings.DATETIME_FORMAT_END)


class CallsConstants():
	def __init__(self):
		pass

	ANSWERED = 'answered'
	INCOMING = 'incoming'
	COMING = 'coming'
	INTERNAL = 'internal'
	CALLBACK = 'callback'

	FAIL_TYPES = ['busy', 'cancel', 'no answer', 'failed', 'no money', 'unallocated number', 'no limit', 'no day limit', 'line limit', 'no money, no limit']


class CommonService():
	def __init__(self):
		pass

	@staticmethod
	def get_random_string(length, only_letters=False, only_digits=False):
		"""
		Generate random string form ascii letters and/or numbers
		:param length: length of string
		:param only_letters: boolean set if the string must contain only letters
		:param only_digits: boolean set if the string must contain only digits
		:return: string
		"""
		if only_letters:
			return crypto.get_random_string(length, string.ascii_letters)
		if only_digits:
			return crypto.get_random_string(length, string.digits)
		return crypto.get_random_string(length)

	@staticmethod
	def get_guid():
		"""
		Generate GUID
		:return: {str} GUID
		"""
		return str(uuid.uuid4())

	@staticmethod
	def parse_csv(csv_string):
		"""
		Parse csv string into array of objects
		:param csv_string: data string
		:return: array of object
		"""
		arr = []
		delimiter = settings.DELIMITER
		csv_string = csv_string[:-1] if csv_string[-1] == '\n' else csv_string
		iter_csv = iter(csv_string.split('\n'))
		next(iter_csv)
		for item in iter_csv:
			arr.append(item.split(delimiter))
		return arr

	@staticmethod
	def parse_form_errors(errors):
		"""
		Parse form errors to the array of string
		:param errors: errors dictionary
		:return: dct - dictionary
		"""
		dct = {}
		for error in errors:
			for key, value in error.iteritems():
				dct[key] = value
		return dct

	@staticmethod
	def is_dates_equals(date1, date2, with_sec):
		"""
		Check if the dates are equals with error
		:param date1: DateTime
		:param date2: DateTime
		:param with_sec: comparison by secs
		:return: Boolean
		"""
		if with_sec:
			return abs(date1 - date2).seconds <= settings.TIME_CORRECTION_SEC
		return date1.date() == date2.date() and date1.hour == date2.hour and abs(date1.minute - date2.minute) <= settings.TIME_CORRECTION_MIN

	@staticmethod
	def write_temp_file(file_instance):
		"""
		Write the file to the filesystem
		:param file_instance: File instance
		:return: path to the file
		"""
		folder_path = os.path.join(settings.BASE_DIR, settings.TEMP_DIR)
		file_path = '%s%s' % (folder_path, file_instance.filename)
		try:
			if not os.path.exists(folder_path):
				os.makedirs(folder_path)
			open(file_path, 'wb').write(file_instance.content)
			return file_path
		except Exception as e:
			logger = LogService()
			logger.error(Code.WRITE_TEMP_FILE_ERR, message=str(e), file_path=file_path)
			return None

	@staticmethod
	def delete_temp_file(filename):
		"""
		Delete temp file from the filesystem
		:param filename: name of the file
		:return:
		"""
		try:
			os.remove(os.path.join(settings.BASE_DIR, settings.TEMP_DIR) + filename)
		except Exception as e:
			logger = LogService()
			logger.warning(Code.WRITE_TEMP_FILE_ERR, message=str(e), file_path=filename)

	@staticmethod
	def convert_to_mp3(file_instance, target_format='mp3', delete_source=True):
		"""
		Convert audio file to mp3
		:param file_instance: source file instance
		:param target_format: format to convert
		:param delete_source: flag to delete source instance after convert succeed
		:return: File instance
		"""
		try:
			audio_mp3 = File(filename=file_instance.filename.replace('.wav', '.' + target_format), path=file_instance.path.replace('.wav', '.' + target_format))
			audio_mp3.content = AudioSegment.from_wav(file_instance.path).export(audio_mp3.path, format=target_format, bitrate='16k')

			if delete_source:
				CommonService.delete_temp_file(file_instance.filename)

			return audio_mp3
		except Exception as e:
			logger = LogService()
			logger.error(Code.CONVERT_TO_MP3_ERR, message=str(e))
			return None

	@staticmethod
	def get_params_string(params):
		"""
		Generate request string from parameters
		:return: request string
		"""
		return urllib.urlencode(sorted(filter(lambda item: item[1], params.items())))

	@staticmethod
	def sha_encode(params_string, method_name, api_version, secret_key):
		"""
		Encode string with sha1 algorithm with secret key
		:param method_name: api method name
		:param secret_key: user secret key to api access
		:return: sha1 encoded string
		"""
		return hmac.new(secret_key.encode(), '%s%s%s%s' % (api_version, method_name, params_string, hashlib.md5(params_string).hexdigest()), hashlib.sha1).hexdigest()

	@staticmethod
	def get_sign(params, method, api_version, secret_key):
		"""
		Generate authorization sigh
		:param method: api method
		:param secret_key: api secret key
		:return: base64 encoded string
		"""
		params_string = CommonService.get_params_string(params.params) if params else ''
		sha_string = CommonService.sha_encode(params_string, method, api_version, secret_key)
		return b64encode(sha_string)

	@staticmethod
	def add_months(source_date, months):
		"""
		Add the number of month to source date
		:param source_date: date
		:param months: number of month
		:return: datetime
		"""
		month = source_date.month - 1 + months
		year = int(source_date.year + month / 12)
		month = month % 12 + 1
		day = min(source_date.day, calendar.monthrange(year, month)[1])
		return datetime.datetime(year, month, day, source_date.hour, source_date.minute, source_date.second)

	@staticmethod
	def define_page(data, page_number, page_data_length=5, data_field_name=None):
		"""
		Divide data to the pages
		:param data: data to divide
		:param page_number: page number
		:param page_data_length: length of the data on the page
		:param data_field_name: returned data field name
		:return: dict of pager data
		"""
		page_number = int(page_number or 1)

		total_count = len(data)
		total_pages = int(math.ceil(float(total_count) / page_data_length))
		return {
			data_field_name or 'data': data[(page_number - 1) * page_data_length:page_number * page_data_length],
			'pages': range(1 if page_number <= 4 else page_number - 3, page_number + 4 if page_number + 4 <= total_pages else total_pages + 1),
			'total_pages': total_pages,
			'current_page_number': page_number,
			'pager_end_helper_stop': total_pages - 3,
		}

	@staticmethod
	def reduce_number(number):
		"""
		Reduce + symbol of phone number
		:param number:
		:return: string
		"""
		return number[1:] if type(number) is str and len(number) == 0 and number[0] == '+' else number