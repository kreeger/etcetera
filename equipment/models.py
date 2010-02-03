import datetime as dt

from django.db import models
from django.contrib.auth import models as auth

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
	
	# Keep trying to have unique=True but Adam keeps wanting to change it
	barcode = models.CharField(
		blank=True,
		null=True,
		max_length=6,
	)
	smsu_id = models.CharField(blank=True, max_length=8)
	equipment_type = models.ForeignKey(EquipmentType) #req
	building = models.ForeignKey(
		Building,
		null=True,
		blank=True,
		related_name='equipments',
	)
	room = models.CharField(blank=True, max_length=15)
	status = models.CharField(blank=True, max_length=15,
		choices=constants.EQUIPMENT_STATUSES)
	serial = models.CharField(blank=True, max_length=100)
	video_unit = models.IntegerField(blank=True, null=True, max_length=5)
	cc_unit = models.IntegerField(
		"computer cart unit",
		blank=True,
		null=True,
		max_length=5
	)
	property_control = models.IntegerField(blank=True, null=True, max_length=5)
	lamp_type = models.CharField(blank=True, max_length=5)
	last_inventoried = models.DateField(default=dt.datetime.today,
		blank=True, null=True) #req
	custname = models.CharField(blank=True, max_length=100) #for legacy support
	department = models.CharField(blank=True, max_length=100)
	on_weekly_checklist = models.BooleanField(default=False) #req
	make = models.ForeignKey(Make, null=True, blank=True)
	model = models.CharField(blank=True, max_length=100)
	received_from = models.CharField(blank=True, max_length=100)
	received_date = models.DateField(default=dt.datetime.today,
		blank=True, null=True)
	value = models.DecimalField(max_digits=7, decimal_places=2, null=True)
	dof = models.CharField(blank=True, max_length=50)
	purchase_order = models.CharField(blank=True, max_length=15)
	budget = models.CharField("funding source", blank=True,
		max_length=10, choices=constants.FUNDING_SOURCES)
	comments = models.TextField(blank=True)
	ticket = models.IntegerField(blank=True, null=True)
	checkout_to = models.CharField(blank=True, max_length=150)

	class Meta:
		verbose_name_plural = 'equipment'
		ordering = (
			'building',
			'room',
			'equipment_type',
			'barcode',
			'smsu_id',
			'make',
			'model',
		)

	def __unicode__(self):
		return u"%s %s (%s %s)" % \
			(self.make, self.model, self.equipment_type, self.barcode)
	
	# What fun! We're overriding save. For logging changes.
	def save(self, force_insert=False, force_update=False):
		# This checks to see if this an update, and not brand new.
		if self.pk is not None:
			# Get original values
			orig = Equipment.objects.filter(pk=self.pk).values()[0]
			# For each entry in the original data
			for key in orig:
				new = getattr(self, key)
				old = orig[key]
				# If nothing was there to begin with, then nothing will stay
				if type(old) == unicode and old == None:
					old = u''
				# This is for logging things that have changed
				if not new == old:
					log = EquipmentLog()
					log.equipment = self
					log.field = unicode(key)
					log.old = unicode(old)
					log.new = unicode(new)
					log.datetime = dt.datetime.now()
					log.save()
		# Also, if barcode is blank upon submission, set it to None
		# This helps to not break duplicate barcodes
		if self.barcode == "":
			self.barcode = None
		# Call super.save
		super(Equipment, self).save(force_insert, force_update)

class EquipmentLog(models.Model):
	"""Logs for when equipment is updated."""
	
	equipment = models.ForeignKey(Equipment, related_name="logs",)
	field = models.CharField(max_length=100)
	old = models.CharField(max_length=200)
	new = models.CharField(max_length=200)
	user = models.ForeignKey(auth.User, null=True)
	datetime = models.DateTimeField(default=dt.datetime.now)

	def __unicode__(self):
		return u"EquipmentLog"
