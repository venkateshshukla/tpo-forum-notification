import os
import re
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
	title = CharField(max_length=128)
	url = CharField()
	next = ForeignKeyField('self', null=True, related_name='prev')

	@classmethod
	@db.atomic()
	def from_dict(cls, at):
		return cls.create(title=at['title'], url=at['url'], next=None)

	@staticmethod
	def from_list(ats):
		logging.debug("Received %d attachments.", len(ats))

		count = 0
		sl = None
		at = None
		for a in reversed(ats):
			at = Attachment.from_dict(a)
			at.next = sl
			at.save()
			sl = at.id
		return at

class Notice(BaseModel):
	title = CharField(max_length=128, index=True)
	url = CharField(max_length=64)
	text = TextField(null=True)
	print_time = CharField(max_length=32)
	updated = BooleanField(default=False, index=True)
	sent = BooleanField(default=False, index=True)

	time = DateTimeField(index=True)
	write_time = DateTimeField(default=datetime.now())
	update_time = DateTimeField(null=True, default=None)
	send_time = DateTimeField(null=True, default=None)

	attachments = ForeignKeyField(Attachment, related_name='notice',
			null=True)
	num_attachments = IntegerField(default=0)

	@classmethod
	@db.atomic()
	def from_dict(cls, nt):
		return cls.create(
			title=nt['title'],
			url=nt['url'],
			text=nt['text'],
			print_time=nt['print_time'],
			sent=nt['sent'],
			time=nt['time'],
			num_attachments=nt['num_attachments'],
			attachments=nt['attachments'])

def get_datetime(s):
	"""
	Extract datetime object from a time string as on TPO Forum.
	"""
	s = re.sub('(st|nd|rd|th),', ',', s)
	d = datetime.strptime(s, "%a %b %d, %Y %I:%M %p")
	return d

class NoticeWrapper(object):
	@staticmethod
	def insert_dict(notice):
		"""
		Given a notice dict with the details, insert it into the Notice
		database
		"""
		notice['print_time'] = notice['time']
		notice['time'] = get_datetime(notice['print_time'])
		if notice['updated']:
			text = notice['text']
			if num_attachments == 0:
				notice['attachments'] = None
			else:
				ats = notice['attachments']
				notice['attachments'] = Attachment.from_list(ats)
		else:
			notice['text'] = None
			notice['attachments'] = None

		if Notice.from_dict(notice):
			return True
		else:
			return False

	@staticmethod
	def insert_dict_safe(notice):
		"""
		Given a dict with details, insert it into Notice database only
		if it is not already present.
		"""
		q = Notice.select().where(Notice.title ==
				notice['title']).exists()
		if q:
			return False
		else:
			return NoticeWrapper.insert_dict(notice)

	@staticmethod
	def get_unupdated():
		"""
		Get all unupdated notices as a list of Notice
		"""
		q = Notice.select().where(Notice.updated ==
				False).order_by(Notice.time)
		return q

	@staticmethod
	def get_unsent():
		"""
		Get all unsent notices as a list of Notice
		"""
		q = Notice.select().where(Notice.sent ==
				False).order_by(Notice.time)
		return q

	@staticmethod
	def update(notice, details):
		"""
		For given Notice, update the entry in database with given
		details
		"""
		notice.text = details['text']
		if notice.num_attachments > 0:
			notice.attachments = Attachment.from_list(details['attachments'])
			notice.num_attachments = len(details['attachments'])
		notice.updated = True
		notice.update_time = datetime.now()
		notice.save()

	@staticmethod
	def sent(notice):
		"""
		Given Notice object is sent to user, update the database to show
		this.
		A little difference (millisecs) in timestamp would not hurt.
		"""
		notice.sent = True
		notice.send_time = datetime.now()
		notice.save()

	@staticmethod
	def get_last(num=25):
		"""
		Return a list of num latest notices.
		The tiny code here was obtained from IRC by cliefer, admin of
		#peewee (most probably the founder).
		It uses subquery to get the result.
		"""
		sq = Notice.select(Notice).order_by(Notice.time.desc()).limit(num)
		sq = sq.alias('t1')
		q = Notice.select().from_(sq).order_by(sq.c.time.asc())
		return q

	@staticmethod
	def init_db():
		db.connect()
		db.create_tables([Attachment, Notice], safe=True)

	@staticmethod
	def deinit_db():
		db.close()
