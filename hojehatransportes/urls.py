from django.conf.urls import *
from hojehatransportes.hat.feeds import RssFeed, IcsFeed, AtomFeed
from django.views.generic import TemplateView, RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^/home', include('hojehatransportes.hat.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'hojehatransportes.hat.views.index'),
    (r'^upgoat', 'hojehatransportes.hat.views.upvote'),
    (r'^downgoat', 'hojehatransportes.hat.views.downvote'),
    (r'^login$', 'hojehatransportes.hat.views.login'),
    (r'^logout$', 'hojehatransportes.hat.views.logout'),
    (r'', include('social.apps.django_app.urls')),
    (r'^submit$', 'hojehatransportes.hat.views.submit'),
    (r'^edit/(?P<strike_id>\d+)$', 'hojehatransportes.hat.views.edit'),
    (r'^thanks', 'hojehatransportes.hat.views.thanks'),
    (r'^submissions$', 'hojehatransportes.hat.views.submissions'),
    (r'^profile$', 'hojehatransportes.hat.views.index'),
    (r'^rss', RssFeed()),
    (r'^atom', AtomFeed()),
    (r'^ics', IcsFeed()),
    (r'^strike/(?P<highlight>\d+)$', 'hojehatransportes.hat.views.index', {}, 'strike_view'),
    (r'^api', include('hojehatransportes.hat.api.urls')),
    (r'^api/', include('hojehatransportes.hat.api.urls')),
    (r'^history', 'hojehatransportes.hat.views.history'),
    (r'^humans.txt', RedirectView.as_view(url='/static/humans.txt')),
    (r'', TemplateView.as_view(template_name='404.html'))
)
