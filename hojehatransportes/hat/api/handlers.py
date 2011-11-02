from piston.handler import AnonymousBaseHandler, BaseHandler
from hat.models import Strike

from datetime import datetime

class AnonymousStrikeListHandler:
  model = Strike
  fields = ('company', 'start_date', 'end_date', 'all_day', 'description', 'canceled', 'source_link', 'submitter')
  #exclude = ('id', 'upvotes', 'downvotes', 'approved')

class StrikeListHandler(BaseHandler):
  allowed_methods = ('GET',)

  model = Strike
  fields = ('company', 'start_date', 'end_date', 'all_day', 'description', 'canceled', 'source_link', ('submitter', ('first_name', 'last_name')), ('company', ('name',)))

  def read(self, request, post_slug=None):
    """
    Returns the strike list with the next scheduled strikes.
    Both canceled and not canceled.
    """

    anonymous = AnonymousBaseHandler

    return Strike.objects.filter(end_date__gte=datetime.today().date()).order_by('start_date').exclude(approved=False)

