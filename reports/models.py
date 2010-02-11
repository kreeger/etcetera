import datetime as dt

from django.db import models
from django.contrib.auth import models as auth
from django.template.defaultfilters import slugify

from etcetera.structure import models as structure
from etcetera.equipment import models as equipment

# Create your models here.
class Report(models.Model):
	"""A basic report."""
	name = models.CharField(max_length=255)
	slug = models.SlugField(unique=True)
	start_date = models.DateTimeField(blank=True)
	end_date = models.DateTimeField(blank=True, default=dt.datetime.now)
	created_by = models.ForeignKey(
		auth.User,
		related_name='reports',
		null=True,
	)
	organizationalunits = models.ManyToManyField(
		structure.OrganizationalUnit,
		related_name='reports',
		null=True, blank=True,
	)
	buildings = models.ManyToManyField(
		structure.Building,
		related_name='reports',
		null=True, blank=True,
	)
	equipmenttypes = models.ManyToManyField(
		equipment.EquipmentType,
		related_name='reports',
		null=True, blank=True,
	)
	
	def __unicode__(self):
		return u"%s" % (self.name,)
	
	def save(self, user=None, *args, **kwargs):
		self.slug = slugify(self.name)
		if user:
			self.created_by = user
		super(Report, self).save(*args, **kwargs)
	
