from django.conf.urls.defaults import *
from hat.feeds import RssFeed, IcsFeed, AtomFeed

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
    (r'^$', 'hat.views.index'),
    (r'^upgoat', 'hat.views.upvote'),
    (r'^downgoat', 'hat.views.downvote'),
    (r'^submit$', 'hat.views.submit'),
    (r'^thanks', 'hat.views.thanks'),
    (r'^rss', RssFeed()),
    (r'^atom', AtomFeed()),
    (r'^ics', IcsFeed()),
    (r'^strike/(?P<highlight>\d+)$', 'hat.views.index', {}, 'strike_view'),
)
