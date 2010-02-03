import datetime as dt

from django.db import models
from django.contrib.auth import models as auth

from etcetera.structure import models as structure
from etcetera.equipment import models as equipment

# Create your models here.
class Report(models.Model):
	"""A basic report."""
	name = models.CharField(max_length=255)
	start_date = models.DateTimeField(blank=True)
	end_date = models.DateTimeField(blank=True, default=dt.datetime.now)
	created_by = models.ForeignKey(
		auth.User,
		related_name='reports',
	)
	organizationalunits = models.ManyToManyField(
		structure.OrganizationalUnit,
		related_name='reports',
	)
	buildings = models.ManyToManyField(
		structure.Building,
		related_name='reports',
	)
	equipmenttypes = models.ManyToManyField(
		equipment.EquipmentType,
		related_name='reports',
	)
	
	def __unicode__(self):
		return u"%s" % (self.name,)
	
