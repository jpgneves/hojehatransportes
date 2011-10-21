# -*- coding: utf-8 -*-
from django.utils import feedgenerator, tzinfo
from django.utils.encoding import force_unicode, iri_to_uri, smart_unicode
from django.template import loader, TemplateDoesNotExist, RequestContext
from django.conf import settings
from django.contrib.sites.models import Site, RequestSite

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
     return Strike.objects.filter(start_date__gte=datetime.today().date()).order_by('start_date')[:10]


# LolFeed: Because "lol, Django". Search for CHANGE
class LolFeed(Feed):
  def get_feed(self, obj, request):
        """
        Returns a feedgenerator.DefaultFeed object, fully populated, for
        this feed. Raises FeedDoesNotExist for invalid parameters.
        """
        #print "ARGH! ",
        #print Site._meta.installed,
        #print " (" + str(Site.objects.get_current()) + "), )",
        #print ", ",
        #print RequestSite(request)
        #if Site._meta.installed:
        #    current_site = Site.objects.get_current()
        #else:
        current_site = RequestSite(request)

        link = self.__get_dynamic_attr('link', obj)
        link = add_domain(current_site.domain, link)

        feed = self.feed_type(
            title = self.__get_dynamic_attr('title', obj),
            subtitle = self.__get_dynamic_attr('subtitle', obj),
            link = link,
            description = self.__get_dynamic_attr('description', obj),
            language = settings.LANGUAGE_CODE.decode(),
            feed_url = add_domain(current_site.domain,
                    self.__get_dynamic_attr('feed_url', obj) or request.path),
            author_name = self.__get_dynamic_attr('author_name', obj),
            author_link = self.__get_dynamic_attr('author_link', obj),
            author_email = self.__get_dynamic_attr('author_email', obj),
            categories = self.__get_dynamic_attr('categories', obj),
            feed_copyright = self.__get_dynamic_attr('feed_copyright', obj),
            feed_guid = self.__get_dynamic_attr('feed_guid', obj),
            ttl = self.__get_dynamic_attr('ttl', obj),
            **self.feed_extra_kwargs(obj)
        )

        title_tmp = None
        if self.title_template is not None:
            try:
                title_tmp = loader.get_template(self.title_template)
            except TemplateDoesNotExist:
                pass

        description_tmp = None
        if self.description_template is not None:
            try:
                description_tmp = loader.get_template(self.description_template)
            except TemplateDoesNotExist:
                pass

        for item in self.__get_dynamic_attr('items', obj):
            if title_tmp is not None:
                title = title_tmp.render(RequestContext(request, {'obj': item, 'site': current_site}))
            else:
                title = self.__get_dynamic_attr('item_title', item)
            if description_tmp is not None:
                description = description_tmp.render(RequestContext(request, {'obj': item, 'site': current_site}))
            else:
                description = self.__get_dynamic_attr('item_description', item)
            link = add_domain(current_site.domain, self.__get_dynamic_attr('item_link', item))
            enc = None
            enc_url = self.__get_dynamic_attr('item_enclosure_url', item)
            if enc_url:
                enc = feedgenerator.Enclosure(
                    url = smart_unicode(enc_url),
                    length = smart_unicode(self.__get_dynamic_attr('item_enclosure_length', item)),
                    mime_type = smart_unicode(self.__get_dynamic_attr('item_enclosure_mime_type', item))
                )
            author_name = self.__get_dynamic_attr('item_author_name', item)
            if author_name is not None:
                author_email = self.__get_dynamic_attr('item_author_email', item)
                author_link = self.__get_dynamic_attr('item_author_link', item)
            else:
                author_email = author_link = None

            pubdate = self.__get_dynamic_attr('item_pubdate', item)
            if pubdate and not pubdate.tzinfo:
                ltz = tzinfo.LocalTimezone(pubdate)
                pubdate = pubdate.replace(tzinfo=ltz)

            feed.add_item(
                title = title,
                link = link,
                description = description,
                unique_id = self.__get_dynamic_attr('item_guid', item, link),
                enclosure = enc,
                pubdate = pubdate,
                author_name = author_name,
                author_email = author_email,
                author_link = author_link,
                categories = self.__get_dynamic_attr('item_categories', item),
                item_copyright = self.__get_dynamic_attr('item_copyright', item),
                **self.item_extra_kwargs(item)
            )
        return feed

def add_domain(domain, url):
    if not (url.startswith('http://')
            or url.startswith('https://')
            or url.startswith('mailto:')):
        # 'url' must already be ASCII and URL-quoted, so no need for encoding
        # conversions here.
        url = iri_to_uri(u'http://%s%s' % (domain, url))
    return url




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
        return strike.get_absolute_url().replace('example', 'hagreve')

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
        return filter((lambda x: not x.canceled), strikeItems())

    def item_summary(self, strike):
        return 'Greve da ' + strike.company.name + ' - ' + strike.region.name

    def item_title(self, strike):
        return strike.company.name + ' - ' + strike.region.name

    def item_start(self, strike):
        if strike.start_date == strike.end_date or strike.all_day:
          return strike.start_date.date()
        return strike.start_date.replace(tzinfo=tzlx)

    def item_end(self, strike):
        if strike.all_day or strike.start_date == strike.end_date:
          return strike.start_date.date() + timedelta(days=1)
        return strike.end_date.replace(tzinfo=tzlx)

    def item_description(self, strike):
        return self.item_comment(strike)

    def item_comment(self, strike): #TODO: Correct this for all-day events
        if strike.all_day:
          return 'Greve da ' + strike.company.name + '\n' + 'Todo o dia ' + str(strike.start_date.date()) + '\n' + strike.description
        return 'Greve da ' + strike.company.name + '\n' + 'De ' + str(strike.start_date) + ' a ' + str(strike.end_date) + '\n' + strike.description

    #def item_link(self, strike):
    #    return strike.get_absolute_url().replace('example', 'hagreve')

