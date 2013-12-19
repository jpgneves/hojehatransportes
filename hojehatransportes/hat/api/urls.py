from django.conf.urls.defaults import *
from piston.resource import Resource
from hat.api.handlers import StrikeListHandler
from hat.api.handlers import AllStrikeListHandler
from django.views.generic import TemplateView

strikelist_handler = Resource(StrikeListHandler)
allstrikelist_handler = Resource(AllStrikeListHandler)

urlpatterns = patterns('',
  url(r'^v1/strikes', strikelist_handler),
  url(r'^v2/strikes', strikelist_handler),
  url(r'^v2/allstrikes', allstrikelist_handler),
)

urlpatterns += patterns('',
    (r'^$', TemplateView.as_view(template_name='api.html')),
)