from django.db import models
from django.contrib.localflavor.us import models as lfus
from django.contrib.auth import models as auth
from etcetera.structure import models as structure
from etcetera.equipment import models as equipment
from etcetera.extras import constants
import datetime as dt

# Create your models here.
class WorkOrder(models.Model):
	"""A work order."""
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	department = models.CharField(max_length=100, blank=True)
	phone = lfus.PhoneNumberField()
	email = models.EmailField(max_length=75)
	equipment = models.ForeignKey(equipment.Equipment)
	building = models.ForeignKey(structure.Building, null=True, blank=True)
	room = models.CharField(max_length=15, blank=True)
	creation_date = models.DateTimeField(default=dt.datetime.now)
	needed_date = models.DateTimeField(blank=True)
	completion_date = models.DateTimeField(blank=True)
	priority = models.CharField(blank=True, max_length=1, choices=constants.PRIORITIES)
	description = models.TextField()
	actions = models.TextField(blank=True)
	labor = models.FloatField(null=True, blank=True)
	technician = models.ForeignKey(auth.User)
	funding_source = models.CharField(blank=True, max_length=4, choices=constants.FUNDING_SOURCES)
	work_type = models.CharField(max_length=11, choices=constants.WORK_TYPES)
	material_costs = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
	budget = models.CharField(blank=True, max_length=10)
	
	def __unicode__(self):
		return u"WorkOrder"
