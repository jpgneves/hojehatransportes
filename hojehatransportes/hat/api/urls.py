from django.conf.urls import *
from piston.resource import Resource
from hojehatransportes.hat.api.handlers import CompanyHandler
from hojehatransportes.hat.api.handlers import StrikeListHandler
from hojehatransportes.hat.api.handlers import AllStrikeListHandler
from django.views.generic import TemplateView

strikelist_handler = Resource(StrikeListHandler)
allstrikelist_handler = Resource(AllStrikeListHandler)
companies_handler = Resource(CompanyHandler)

urlpatterns = patterns('',
  url(r'^v1/strikes', strikelist_handler),
  url(r'^v2/strikes', strikelist_handler),
  url(r'^v2/allstrikes', allstrikelist_handler),
  url(r'^v2/companies', companies_handler)
)

urlpatterns += patterns('',
  (r'^$', TemplateView.as_view(template_name='api.html')),
)
