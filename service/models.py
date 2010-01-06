import datetime as dt

from django.db import models
from django.contrib.localflavor.us import models as lfus
from django.contrib.auth import models as auth

from etcetera.structure import models as structure
from etcetera.equipment import models as equipment
from etcetera.extras import constants

# Create your models here.
class WorkOrder(models.Model):
	"""A work order."""
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	department = models.CharField(max_length=100, blank=True)
	phone = lfus.PhoneNumberField(blank=True)
	email = models.EmailField(max_length=75, blank=True)
	equipment_text = models.CharField(max_length=75, blank=True)
	equipment = models.ForeignKey(equipment.Equipment, null=True, blank=True)
	building = models.ForeignKey(structure.Building, null=True, blank=True)
	room = models.CharField(max_length=25, blank=True)
	location_text = models.CharField(max_length=75, blank=True, null=True)
	creation_date = models.DateTimeField(default=dt.datetime.now, null=True)
	needed_date = models.DateTimeField(blank=True, null=True)
	completion_date = models.DateTimeField(blank=True, null=True)
	priority = models.CharField(
		blank=True,
		max_length=1,
		choices=constants.PRIORITIES
	)
	description = models.TextField()
	actions = models.TextField('Actions taken', blank=True)
	labor = models.FloatField('Labor hours', null=True, blank=True)
	technician = models.ForeignKey(auth.User, blank=True, null=True)
	tech_legacy = models.CharField(blank=True, max_length=10)
	funding_source = models.CharField(
		blank=True,
		max_length=5,
		choices=constants.FUNDING_SOURCES
	)
	work_type = models.CharField(max_length=11, choices=constants.WORK_TYPES)
	material_costs = models.DecimalField(max_digits=9,
		decimal_places=2,
		blank=True,
		null=True
	)
	budget = models.CharField(blank=True, max_length=25)
	completed = models.BooleanField()
	
	# What fun! We're overriding save. For logging changes.
	def save(self, force_insert=False, force_update=False):
		# Ensure capitalization.
		self.first_name = self.first_name.capitalize()
		self.last_name = self.last_name.capitalize()
		# This checks to see if this an update, and not brand new.
		if self.pk is not None:
			# Get original object
			orig = WorkOrder.objects.get(pk=self.pk)
			# For each entry in the original data
			if self.completed and not orig.completed:
				self.completion_date = dt.datetime.now()
		# Call super.save
		super(WorkOrder, self).save(force_insert, force_update)
	
	def __unicode__(self):
		return u"%s, %s (%s)" % (self.last_name, self.equipment,
			self.creation_date)
	
