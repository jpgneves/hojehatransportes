from django.conf.urls.defaults import *
from piston.resource import Resource
from hat.api.handlers import StrikeListHandler

strikelist_handler = Resource(StrikeListHandler)

urlpatterns = patterns('',
  url(r'^v1/strikes', strikelist_handler),
)
