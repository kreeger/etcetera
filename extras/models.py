import datetime as dt

from django.db import models
from django.contrib.auth import models as auth

class Post(models.Model):
	"""A simple blog post."""
	title = models.CharField(max_length=75)
	pub_date = models.DateTimeField(default=dt.datetime.now)
	content = models.TextField()
	author = models.ForeignKey(auth.User)
	
	class Meta:
		ordering = ('-pub_date',)

	def __unicode__(self):
		return u"%s" % (self.title,)
