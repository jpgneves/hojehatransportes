# coding=utf-8
from models import Strike, Region, Company
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import SortedDict
from django.template import RequestContext
import locale
from datetime import datetime, date, timedelta
import calendar
from operator import itemgetter, attrgetter

locale.setlocale(locale.LC_ALL, "pt_PT.UTF-8")

def index(request):
    latest_strikes = Strike.objects.filter(end_date__gte=datetime.today().date()).order_by('start_date')[:20]
    companies = Company.objects.all()
    regions = Region.objects.all()
    
    strikes = SortedDict()
    
    todaysDay = datetime.today().strftime("%d")
    todayMonth = datetime.today().strftime("%m")
    tomorrow = datetime.today().date() + timedelta(days=1)
    tomorrowsDay = tomorrow.strftime("%d")

    for strike in latest_strikes:
        m = strike.start_date.strftime("%m")
        if m < todayMonth:
            m = todayMonth
        d = strike.start_date.strftime("%d")
        
        if strike.start_date < datetime.today():
            d = todaysDay
        
        if not strikes.has_key(m):
            strikes[m] = {"name":calendar.month_name[int(m)], "days":SortedDict()}
        if not strikes[m]["days"].has_key(d):
            strikes[m]["days"][d] = {'strikes':{}}
        if not strikes[m]["days"][d]['strikes'].has_key(strike.company):
            strikes[m]["days"][d]['strikes'][strike.company] = []
        strikes[m]["days"][d]['strikes'][strike.company].append(strike)


    m = datetime.today().strftime("%m")
    if len(strikes) > 0 and strikes.has_key(m):
        fix = False
        if strikes[m]["days"].has_key(tomorrowsDay):
            strikes[m]["days"][tomorrowsDay]["alias"] = "Amanhã"
            fix = True        

        if strikes[m]["days"].has_key(todaysDay):
            strikes[m]["days"][todaysDay]["alias"] = "Hoje"
            if fix:
                strikes[m]["days"][todaysDay]["fix"] = "fixTomorrow"
            for c in strikes[m]["days"][todaysDay]["strikes"]:
                cc = strikes[m]["days"][todaysDay]["strikes"][c]
                if len(cc) > 1:
                    strikes[m]["days"][todaysDay]["strikes"][c] = sorted(cc, key=MYattrgetter('start_date.day'), reverse=True)

    
    #strikes['04']["days"] = sorted(strikes['04']["days"])


    context = { 'strikes': strikes, 'regions': regions, 'host': request.get_host(), 'companies': companies }
    
    return render_to_response('index.html', context)


def MYattrgetter(*items):
    if len(items) == 1:
        attr = items[0]
        def g(obj):
            return resolve_attr(obj, attr)
    else:
        def g(obj):
            return tuple(resolve_att(obj, attr) for attr in items)
    return g

def resolve_attr(obj, attr):
    for name in attr.split("."):
        obj = getattr(obj, name)
    return obj



def thanks(request):
    return render_to_response('thanks.html')

@require_POST
def upvote(request):
    """Add an upvote to a strike"""
    try:
        strike_id = int(request.POST['strikeid'])
        strike = Strike.objects.get(id=strike_id)
    except KeyError:
        print "Error: bad parameter strikeid"
        return HttpResponseServerError()
    except ObjectDoesNotExist:
        print "Error: strike with id %d does not exist" % strike_id
        return HttpResponseServerError()
    else:
        strike.upvotes += 1
        strike.save()
        return HttpResponse()
    
@require_POST
def downvote(request):
    """Add a downvote to a strike"""
    try:
        strike_id = int(request.POST['strikeid'])
        strike = Strike.objects.get(id=strike_id)
    except KeyError:
        print "Error: bad parameter strikeid"
        return HttpResponseServerError()
    except ObjectDoesNotExist:
        print "Error: strike with id %d does not exist" % strike_id
        return HttpResponseServerError()
    else:
        strike.downvotes += 1
        strike.save()
        return HttpResponse()
        
def submit(request):
    pass
