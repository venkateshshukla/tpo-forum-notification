import os
import logging

from datetime import datetime
from peewee import *
from playhouse.db_url import connect

db_name = os.environ.get('DATABASE_URL')
db = connect(db_name)

class Notice(Model):
	class Meta:
		database = db

	serial = IntegerField(unique=True, primary_key=True)

	title = CharField(max_length=128)
	url = CharField(max_length=64)
	text = TextField(null=True)
	print_time = CharField(max_length=32)
	num_attachments = IntegerField(default=0)
	updated = BooleanField(default=False, index=True)
	sent = BooleanField(default=False, index=True)

	time = DateTimeField(index=True)
	write_time = DateTimeField(default=datetime.now())
	update_time = DateTimeField()
	send_time = DateTimeField()

class NoticeWrapper(object):
	def insert_dict(notice):
		pass
	def update():
		pass
	def get():
		pass

def init_db():
	db.connect()
	db.create_tables([Notice], safe=True)

def deinit_db():
	db.close()

if __name__ == '__main__':
	logging.debug("Starting : {}".format(__file__))
	init_db()
	deinit_db()
