import datetime as dt

from django.db import models
from django.contrib.localflavor.us import models as lfus
from django.contrib.auth import models as auth

from etcetera.structure import models as structure
from etcetera.equipment import models as equipment
from etcetera.extras import constants

class Checkout(models.Model):
	"""An order for checking out equipment."""
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	department_text = models.CharField(
		max_length=100,
		verbose_name="department",
	)
	department = models.ForeignKey(
		structure.OrganizationalUnit,
		null=True,
		blank=True
	)
	course = models.CharField(
		max_length=20,
		blank=True,
		help_text="If the request is for a specific course, state the course.",
	)
	phone = lfus.PhoneNumberField()
	email = models.EmailField(max_length=75)
	equipment_needed = models.TextField()
	building = models.ForeignKey(
		structure.Building,
		blank=True, null=True,
		related_name='checkouts',
		help_text='The building the equipment will be at for the \
			duration of the checkout.',
	)
	room = models.CharField(max_length=25, blank=True)
	checkout_type = models.CharField(
		max_length=8,
		choices=constants.CHECKOUT_TYPES
	)
	return_type = models.CharField(
		max_length=9,
		choices=constants.RETURN_TYPES
	)
	creation_date = models.DateTimeField(default=dt.datetime.now)
	out_date = models.DateTimeField()
	return_date = models.DateTimeField()
	creating_user = models.ForeignKey(
		auth.User,
		blank=True, null=True,
		related_name="created_checkouts",
	)
	delivering_user = models.ForeignKey(
		auth.User,
		blank=True, null=True,
		related_name="deliveries",
	)
	returning_person = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		verbose_name="returner"
	)
	equipment_list = models.ManyToManyField(
		equipment.Equipment,
		limit_choices_to={
			'status': 'checkout',
		},
		related_name='checkouts',
		blank=True, null=True,
	)
	other_equipment = models.TextField(blank=True)
	software = models.TextField(blank=True)
	completed = models.BooleanField()
	
	def __unicode__(self):
		return u"%s %s, %s" % (
			self.first_name,
			self.last_name,
			self.creation_date
		)
