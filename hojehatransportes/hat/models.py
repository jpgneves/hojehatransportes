from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Company(models.Model):
	""" Represents a company and associated transport type """
	
	TRANSPORT_CHOICES = (
		("T", _("Train")),
		("S", _("Subway")),
		("B", _("Bus")),
		("F", _("Ferry")),
		("A", _("Airplane"))
	)
	
	name = models.CharField(max_length=30)
	transport_type = models.CharField(max_length=1, choices=TRANSPORT_CHOICES)
	
	class Meta:
		verbose_name_plural = "companies"
	
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
	upvotes = models.PositiveIntegerField(default=0)
	downvotes = models.PositiveIntegerField(default=0)
	region = models.ForeignKey(Region)
	canceled = models.BooleanField(default=False)
	source_link = models.URLField(blank=True)
	approved = models.BooleanField(default=False)
	
	def __unicode__(self):
		return "%s - %s : %s" % (self.start_date, self.end_date, self.company)