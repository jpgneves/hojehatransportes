from django.contrib.syndication.views import Feed
from datetime import datetime, date
import locale

from hat.models import Strike, Region

locale.setlocale(locale.LC_ALL, "pt_PT.UTF-8")

class RssFeed(Feed):
    """Generate an RSS of the strikes"""
    title = 'Hoje h&aacute; greve?'
    link = ''
    description = 'Veja se consegue chegar ao trabalho. Lembre-se que as informa&ccedil;&otilde;es podem estar desactualizadas.'

    def items(self):
        return Strike.objects.filter(start_date__gte=datetime.today().date()).order_by('start_date')[:10]

    def item_summary(self, strike):
        return strike.description

    def item_title(self, strike):
        return strike.company.name + ' - ' + strike.region.name

    def item_description(self, strike):
        return strike.description

    def item_link(self, strike):
        return 'https://hagreve.com'

