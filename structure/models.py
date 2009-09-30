from django.db import models
from django.contrib.localflavor.us import models as lfus
from django.contrib.auth.models import User

# Defines university structure regarding people and places.

class OrganizationalUnit(models.Model):
	"""A nestable unit for figuring out who departments and colleges are."""
	name = models.CharField(max_length=100)
	parent = models.ForeignKey(
		'self',
		blank=True, null=True,
		related_name='children',
	)
	abbreviation = models.CharField(max_length=8, blank=True)
	
	class Meta:
		ordering = ('name',)

	def __unicode__(self):
		return u"%s" % (self.name,)

class Campus(models.Model):
	"""A top-level container for building structure"""
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	state = lfus.USStateField()
	zip_code = models.CharField(max_length=9)
	country = models.CharField(max_length=50, default='United States')
	phone = lfus.PhoneNumberField()
	
	def __unicode__(self):
		return u"%s" % self.name
	
	class Meta:
		ordering = ('name',)
		verbose_name_plural = "campuses"

class Building(models.Model):
	"""A level-two container for building structure"""
	name = models.CharField(max_length=100)
	abbreviation = models.CharField(max_length=20, blank=True, unique=True)
	campus = models.ForeignKey(Campus)
	
	class Meta:
		ordering = ('campus', 'name',)
	
	def save(self, *args, **kwargs):
		if not self.abbreviation:
			self.abbreviation = self.name.split()[0]
		super(Building, self).save(*args, **kwargs)
	
	def __unicode__(self):
		return u"%s" % self.name
