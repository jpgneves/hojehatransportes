# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django_cal.views import Events
from datetime import datetime, date
import django_cal
import locale

from hat.models import Strike, Region

locale.setlocale(locale.LC_ALL, "pt_PT.UTF-8")

class RssFeed(Feed):
    """Generate an RSS of the strikes"""
    title = u'Hoje há greve?'
    link = ''
    description = u'Veja se consegue chegar ao trabalho. Lembre-se que as informações podem estar desactualizadas.'

    def items(self):
        return Strike.objects.filter(start_date__gte=datetime.today().date()).order_by('start_date')[:10]

    def item_summary(self, strike):
        return strike.description

    def item_title(self, strike):
        return strike.company.name + ' - ' + strike.region.name

    def item_description(self, strike):
        return 'Greve da empresa ' + strike.company.name + '<br/>' + 'De ' + str(strike.start_date) + ' a ' + str(strike.end_date) + '<br/>' + strike.description

    def item_link(self, strike):
        return 'http://hagreve.com'

    def item_pubdate(self, strike):
        return strike.start_date


class IcsFeed(Events):
    def cal_name(self):
        return u'Hoje há greve?'

    def cal_desc(self):
        return u'Veja se consegue chegar ao trabalho. Lembre-se que as informações podem estar desactualizadas.'

    def items(self):
        return Strike.objects.filter(start_date__gte=datetime.today().date()).order_by('start_date')[:10]

    def item_summary(self, strike):
        return strike.description

    def item_title(self, strike):
        return strike.company.name + ' - ' + strike.region.name

    def item_start(self, strike):
        return strike.start_date

    def item_end(self, strike):
        return strike.end_date

    def item_description(self, strike):
        return 'Greve da empresa ' + strike.company.name + '\n' + 'De ' + str(strike.start_date) + ' a ' + str(strike.end_date.strftime) + '\n' + strike.description

    def item_link(self, strike):
        return 'https://hagreve.com'

