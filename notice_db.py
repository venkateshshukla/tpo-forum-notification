import os
import logging

from datetime import datetime
from peewee import *
from playhouse.db_url import connect

db_name = os.environ.get('DATABASE_URL')
db = connect(db_name)

class BaseModel(Model):
	class Meta:
		database = db

class Attachment(BaseModel):
	serial = IntegerField(unique=True, primary_key=True)
	title = CharField(max_length=128)
	url = CharField()
	next = ForeignKeyField('self', null=True, related_name='prev')

class Notice(BaseModel):
	serial = IntegerField(unique=True, primary_key=True)

	title = CharField(max_length=128, index=True)
	url = CharField(max_length=64)
	text = TextField(null=True)
	print_time = CharField(max_length=32)
	updated = BooleanField(default=False, index=True)
	sent = BooleanField(default=False, index=True)

	time = DateTimeField(index=True)
	write_time = DateTimeField(default=datetime.now())
	update_time = DateTimeField()
	send_time = DateTimeField()

	attachments = ForeignKeyField(Attachment, related_name='notice')
	num_attachments = IntegerField(default=0)

class NoticeWrapper(object):
	def insert_dict(notice):
		"""
		Given a notice dict with the details, insert it into the Notice
		database
		"""
		pass
	def get_unupdated():
		"""
		Get all unupdated notices as a list of Notice
		"""
		pass
	def get_unsent():
		"""
		Get all unsent notices as a list of Notice
		"""
		pass
	def update(notice, details):
		"""
		For givem Notice, update the entry in database with given
		details
		"""
		pass
	def get():
		pass
	def get_last(num=25):
		"""
		Return a list of num latest notices.
		"""
		pass

def init_db():
	db.connect()
	db.create_tables([Attachment, Notice], safe=True)

def deinit_db():
	db.close()

if __name__ == '__main__':
	logging.debug("Starting : {}".format(__file__))
	init_db()
	deinit_db()
