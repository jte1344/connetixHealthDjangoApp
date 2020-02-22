from django.db import models


class Price(models.Model):
    location = models.CharField(max_length=200)
    lookup_date = models.DateTimeField('date')
