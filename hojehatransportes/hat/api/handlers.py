from piston.handler import AnonymousBaseHandler, BaseHandler
from hojehatransportes.hat.models import Strike, Company

from datetime import datetime
from copy import deepcopy

#class AnonymousStrikeListHandler:
  #model = Strike
  #fields = ('id', 'company', 'start_date', 'end_date', 'all_day', 'description', 'canceled', 'source_link', 'submitter')
  #exclude = ('id', 'upvotes', 'downvotes', 'approved')

class CompanyHandler(BaseHandler):
  allowed_methods = ('GET',)

  model = Company
  fields = ('id', 'name')

  def read(self, request, post_slug=None):

    anonymous = AnonymousBaseHandler

    return list(Company.objects.all())


class StrikeListHandler(BaseHandler):
  allowed_methods = ('GET',)

  model = Strike
  fields = ('id', 'company', 'start_date', 'end_date', 'all_day', 'description', 'canceled', 'source_link', ('submitter', ('first_name', 'last_name')), ('company', ('name', 'id')))

  def read(self, request, post_slug=None):
    """
    Returns the strike list with the next scheduled strikes.
    Both canceled and not canceled.
    """

    anonymous = AnonymousBaseHandler

    # tmp = list(Strike.objects.filter(end_date__gte=datetime.today().date()).order_by('start_date').exclude(approved=False))

    tmp = deepcopy(list(Strike.objects.filter(end_date__gte=datetime.today().date()).order_by('start_date').exclude(approved=False)))

    for i in tmp:
      i.end_date = str(i.end_date).replace("T", " ")
      i.start_date = str(i.start_date).replace("T", " ")

    return tmp

class AllStrikeListHandler(BaseHandler):
  allowed_methods = ('GET',)

  model = Strike
  fields = ('id', 'company', 'start_date', 'end_date', 'all_day', 'description', 'canceled', 'source_link', ('submitter', ('first_name', 'last_name')), ('company', ('name', 'id')))

  def read(self, request, post_slug=None):
    """
    Returns the strike list with all strikes.
    Both canceled and not canceled.
    """

    anonymous = AnonymousBaseHandler

    # tmp = list(Strike.objects.filter(end_date__gte=datetime.today().date()).order_by('start_date').exclude(approved=False))

    tmp = deepcopy(list(Strike.objects.order_by('start_date').exclude(approved=False)))

    for i in tmp:
      i.end_date = str(i.end_date).replace("T", " ")
      i.start_date = str(i.start_date).replace("T", " ")

    return tmp

