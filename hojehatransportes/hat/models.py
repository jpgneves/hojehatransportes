from django.db import models

# Create your models here.

class Company(models.Model):
	""" Represents a company """
	name = models.CharField(max_length=30)

class Strike(models.Model):
	""" Represents a strike in a given company """
	company = models.ForeignKey(Company)
	date = models.DateTimeField()
	description = models.CharField(max_length=255)