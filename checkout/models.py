import datetime as dt

from django.db import models
from django.contrib.localflavor.us import models as lfus
from django.contrib.auth import models as auth

from etcetera.structure import models as structure
from etcetera.equipment import models as equipment

class Checkout(models.Model):
	"""An order for checking out equipment."""
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	department = models.ForeignKey(structure.OrganizationalUnit)
	course = models.CharField(max_length=20, blank=True)
	phone = lfus.PhoneNumberField()
	email = models.EmailField(max_length=75)
	equipment_needed = models.TextField()
	building = models.ForeignKey(structure.Building, related_name='checkouts')
	room = models.CharField(max_length=25)
	checkout_type = models.CharField(
		max_length=8,
		choices=constants.CHECKOUT_TYPES
	)
	returner = models.CharField(max_length=9, choices=constants.RETURNERS)
	creation_date = models.DateTimeField(default=dt.datetime.now)
	out_date = models.DateTimeField()
	return_date = models.DateTimeField()
	receiving_user = models.ForeignKey(auth.User, blank=True, null=True)
	delivering_user = models.ForeignKey(auth.User, blank=True, null=True)
	returning_person = models.CharField(max_length=100, blank=True, null=True)
	equipment_list = models.ManyToManyField(
		equipment.Equipment,
		limit_choices_to={
			'status': 'checkout',
		},
		related_name='checkouts',
		blank=True, null=True,
	)
	software = models.TextField(blank=True)
	
	def __unicode__(self):
		return u"%s %s, %s" % (
			self.first_name,
			self.last_name,
			self.creation_date
		)
