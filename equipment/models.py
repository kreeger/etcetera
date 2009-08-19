from django.db import models
import datetime as dt
from etcetera.structure.models import Building
from etcetera.extras import constants

class EquipmentType(models.Model):
	"""A category for the type of equipment"""
	name = models.CharField(max_length=100)
	
	class Meta:
		ordering = ('name',)
	
	def __unicode__(self):
		return u"%s" % self.name

class Make(models.Model):
	name = models.CharField(max_length=100)
	website = models.URLField(blank=True, verify_exists=False)
	
	class Meta:
		ordering = ('name',)
	
	def __unicode__(self):
		return u"%s" % self.name

class Equipment(models.Model):
	"""One item of equipment"""
	
	barcode = models.CharField(blank=True, max_length=6)
	smsu_id = models.CharField(blank=True, max_length=8)
	equipment_type = models.ForeignKey(EquipmentType) #req
	building = models.ForeignKey(Building, null=True, blank=True)
	room = models.CharField(blank=True, max_length=15)
	status = models.CharField(blank=True, max_length=15, choices=constants.EQUIPMENT_STATUSES)
	serial = models.CharField(blank=True, max_length=100)
	video_unit = models.IntegerField(blank=True, null=True, max_length=5)
	property_control = models.IntegerField(blank=True, null=True, max_length=5)
	lamp_type = models.CharField(blank=True, max_length=5)
	last_inventoried = models.DateField(default=dt.datetime.today, blank=True, null=True) #req
	custname = models.CharField(blank=True, max_length=100) #for legacy support
	department = models.CharField(blank=True, max_length=100)
	on_weekly_checklist = models.BooleanField(default=False) #req
	make = models.ForeignKey(Make, null=True, blank=True)
	model = models.CharField(blank=True, max_length=100)
	received_from = models.CharField(blank=True, max_length=100)
	received_date = models.DateField(default=dt.datetime.today, blank=True, null=True)
	value = models.DecimalField(max_digits=7, decimal_places=2, null=True)
	dof = models.CharField(blank=True, max_length=50)
	purchase_order = models.CharField(blank=True, max_length=15)
	budget = models.CharField("Funding sources", blank=True, max_length=10, choices=constants.FUNDING_SOURCES)
	comments = models.TextField(blank=True)
	ticket = models.IntegerField(blank=True, null=True)
	checkout_to = models.CharField(blank=True, max_length=150)

	class Meta:
		verbose_name_plural = 'equipment'
		ordering = ('building','room','equipment_type','barcode','smsu_id','make','model',)

	def __unicode__(self):
		return u"%s %s (%s %s)" % (self.make, self.model, self.equipment_type, self.barcode)
