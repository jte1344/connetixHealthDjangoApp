from django.db import models


class Price(models.Model):
    location = models.CharField(max_length=200)
    medication = models.CharField(max_length=200)
