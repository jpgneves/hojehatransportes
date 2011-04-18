# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django_cal.views import Events
from datetime import datetime, date, timedelta
import django_cal
import locale
import dateutil

from hat.models import Strike, Region

locale.setlocale(locale.LC_ALL, "pt_PT.UTF-8")

tzlx = dateutil.tz.gettz('Europe/Lisbon')

def strikeItems():
    return Strike.objects.filter(start_date__gte=datetime.today().date()).exclude(canceled=True).order_by('start_date')[:10]


class RssFeed(Feed):
    """Generate an RSS of the strikes"""
    title = u'Hoje há greve?'
    link = 'http://hagreve.com'
    description = u'Veja se consegue chegar ao trabalho. Lembre-se que as informações podem estar desactualizadas.'
    author_name = 'hagreve.com'
    author_link = 'http://hagreve.com'
    author_email = 'info@hagreve.com'
    copyright = 'hagreve.com, ' + str(datetime.now().year)

    def items(self):
        return strikeItems().reverse()

    def item_title(self, strike):
        return strike.company.name + ' - ' + strike.region.name

    description_template = 'feeds/rss_description.html'

    def item_summary(self, strike):
        return strike.company.name + ' - ' + strike.region.name

    def item_link(self, strike):
        return 'http://hagreve.com'

    def item_pubdate(self, strike):
        return strike.start_date

class AtomFeed(RssFeed):
    feed_type = Atom1Feed
    subtitle = RssFeed.description

class IcsFeed(Events):
    filename = 'greves.ics'

    def cal_name(self):
        return u'Hoje há greve?'

    def cal_desc(self):
        return u'Veja se consegue chegar ao trabalho. Lembre-se que as informações podem estar desactualizadas.'

    def items(self):
        return strikeItems()

    def item_summary(self, strike):
        return 'Greve da ' + strike.company.name + ' - ' + strike.region.name

    def item_title(self, strike):
        return strike.company.name + ' - ' + strike.region.name

    def item_start(self, strike):
        if strike.start_date == strike.end_date or strike.all_day:
          return strike.start_date.date()
        return strike.start_date.replace(tzinfo=tzlx)

    def item_end(self, strike):
        if strike.start_date == strike.end_date or strike.all_day:
          return strike.end_date.date() + timedelta(days=1)
        return strike.end_date.replace(tzinfo=tzlx)

    def item_description(self, strike):
        return self.item_comment(strike)

    def item_comment(self, strike): #TODO: Correct this for all-day events
        return 'Greve da ' + strike.company.name + '\n' + 'De ' + str(strike.start_date) + ' a ' + str(strike.end_date) + '\n' + strike.description

    def item_link(self, strike):
        return 'https://hagreve.com'

