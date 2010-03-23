import datetime as dt

from django.db import models
from django.contrib.auth import models as auth
from django.contrib.localflavor.us import models as lfus

from etcetera.structure import models as structure

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

class UserProfile(models.Model):
    """A user profile."""
    user = models.ForeignKey(auth.User, unique=True, null=True)
    title = models.CharField('Title', blank=True, max_length=100)
    phone = lfus.PhoneNumberField('Phone', blank=True)
    image = models.ImageField('Profile image',upload_to="photos", blank=True, null=True)
    office_building = models.ForeignKey(
        structure.Building,
        null=True,
        blank=True
    )
    office_room = models.CharField(blank=True, max_length=20)
    
    def __unicode__(self):
        return u"%s %s's Profile" % (self.user.first_name, self.user.last_name)