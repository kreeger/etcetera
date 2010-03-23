import datetime as dt

from django.db import models

class CheckoutManager(models.Manager):
    def active(self):
        return self.get_query_set().filter(completion_date=None)
    
    def closed(self):
        return self.get_query_set().exclude(completion_date=None)