import logging
import datetime

from django.core.management.base import NoArgsCommand

from etcetera.checkout.models import Checkout

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		# Save the current date/time in a variable
		now = datetime.datetime.now()
		
		# Set logging level
		logging.basicConfig(
			level=logging.DEBUG,
			format='%(asctime)s %(levelname)s %(message)s',
		)
		
		# For current checkouts, set related equipment status to checkedout
		for checkout in Checkout.objects.filter(
			out_date__lte=now).filter(
			return_date__gte=now).filter(
			completed=False):
			for eq in checkout.equipment_list.all():
				if eq.status == 'reserved':
					eq.status = 'checkedout'
					eq.save()
