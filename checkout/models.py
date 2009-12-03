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
		verbose_name='department',
		help_text='The university department the request should be under.',
	)
	department = models.ForeignKey(
		structure.OrganizationalUnit,
		null=True,
		blank=True,
	)
	course = models.CharField(
		max_length=20,
		blank=True,
		help_text='If the request is for a specific course, state the course.',
	)
	phone = lfus.PhoneNumberField(help_text='Format: ###-###-####',)
	# should be required soon
	email = models.EmailField(
		blank=True,
		max_length=75,
		help_text='Your university email address.',
	)
	equipment_needed = models.TextField(
		help_text='Give a clear description of the equipment you would like \
		to reserve, as well as any specific models if desired.',
	)
	building = models.ForeignKey(
		structure.Building,
		blank=True, null=True,
		related_name='checkouts',
		help_text='The building the equipment will be at for the \
			duration of the checkout.',
	)
	room = models.CharField(
		max_length=25,
		blank=True,
		help_text='The room in the building specified above.',
	)
	checkout_type = models.CharField(
		max_length=8,
		choices=constants.CHECKOUT_TYPES,
		verbose_name='Pickup/delivery?',
		help_text='Will this ticket be picked up or delivered by ETC?',
	)
	return_type = models.CharField(
		max_length=9,
		choices=constants.RETURN_TYPES,
		verbose_name='Who will return?',
		help_text='Will you be returning the equipment, or will ETC be \
			picking it up?',
	)
	creation_date = models.DateTimeField(default=dt.datetime.now)
	out_date = models.DateTimeField(
		verbose_name='Pickup/delivery date',
		help_text='The date/time you will pick up the equipment, or \
			when ETC should deliver it.',
	)
	return_date = models.DateTimeField(
		help_text='The date/time you will bring back the equipment, or when \
			ETC should pick it up.',
	)
	creating_user = models.ForeignKey(
		auth.User,
		blank=True, null=True,
		related_name='created_checkouts',
	)
	delivering_user = models.ForeignKey(
		auth.User,
		blank=True, null=True,
		related_name='deliveries',
	)
	returning_person = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		verbose_name='returner'
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
	completed = models.BooleanField()
	completion_date = models.DateTimeField(blank=True, null=True)
	comments = models.TextField(blank=True)
	
	class Meta:
		ordering = (
			'first_name',
			'last_name',
			'out_date',
			'return_date',
		)
	
	def __unicode__(self):
		return u'%s %s, %s' % (
			self.first_name,
			self.last_name,
			self.creation_date
		)
