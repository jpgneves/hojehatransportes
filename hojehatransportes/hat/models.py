from django.db import models

# Create your models here.

class Company(models.Model):
	""" Represents a company and associated transport type """
	
	TRANSPORT_CHOICES = (
		("T", "Train"),
		("S", "Subway"),
		("B", "Bus"),
		("F", "Ferry"),
		("A", "Airplane")
	)
	
	name = models.CharField(max_length=30)
	transport_type = models.CharField(max_length=1, choices=TRANSPORT_CHOICES)
	
	def __unicode__(self):
		return self.name

class Region(models.Model):
	"""Represents a region"""
	
	name = models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.name
		

class Strike(models.Model):
	""" Represents a strike entry in a given company """
	
	company = models.ForeignKey(Company)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	description = models.CharField(max_length=255)
	upvotes = models.PositiveIntegerField()
	downvotes = models.PositiveIntegerField()
	region = models.ForeignKey(Region)
	
	def __unicode__(self):
		return "%s - %s : %s" % (self.start_date, self.end_date, self.company)