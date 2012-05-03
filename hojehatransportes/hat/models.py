# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

# Create your models here.

class Company(models.Model):
    """ Represents a company """
    
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=30)
        
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
    end_date = models.DateTimeField(blank=True, null=True)
    all_day = models.BooleanField(default=False)
    description = models.CharField(max_length=255)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    region = models.ForeignKey(Region)
    canceled = models.BooleanField(default=False)
    source_link = models.URLField(blank=True)
    approved = models.BooleanField(default=False)
    submitter = models.ForeignKey(User, default=1)
    
    def __unicode__(self):
        return "%s - %s : %s" % (self.start_date, self.end_date, self.company)
    
    def __unicode__(self):
        description = unicode(self.description)
        if len(description) > 30:
            description = description[0:30] + u"…"
        c = unicode(self.company)
        return "%s : %s - %s" % (self.start_date, c, description)
    
    # Model validation
    def clean(self):
        # Don't allow start dates after end dates
        if self.start_date > self.end_date:
            raise ValidationError('Start date cannot be after end date')
        
        # Don't allow strikes starting in the past (in days)
        if self.start_date.date() < datetime.today().date():
            raise ValidationError('Strike cannot start in the past')

    @models.permalink
    def get_absolute_url(self):
        return ('strike_view',  [str(self.id)])
    #def get_absolute_url(self):
    #    return '/s/' + str(self.id)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    mail_notifications = models.BooleanField(default=False)
