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

def index(request, highlight='-1'):
    latest_strikes = Strike.objects.filter(end_date__gte=datetime.today().date()).order_by('start_date')[:20]
    companies = Company.objects.all()
    regions = Region.objects.all()
    
    strikes = SortedDict()
    
    hoje = datetime.today().strftime("%d")
    todayMonth = datetime.today().strftime("%m")
    amanha = datetime.today().date() + timedelta(days=1)
    amanha = amanha.strftime("%d")

    for strike in latest_strikes:
        m = strike.start_date.strftime("%m")
        if m < todayMonth:
            m = todayMonth
        d = strike.start_date.strftime("%d")
        
        if strike.start_date < datetime.today():
            d = hoje
        
        if not strikes.has_key(m):
            strikes[m] = {"nome":calendar.month_name[int(m)], "dias":SortedDict()}
        if not strikes[m]["dias"].has_key(d):
            strikes[m]["dias"][d] = {'greves':{}}
        if not strikes[m]["dias"][d]['greves'].has_key(strike.company):
            strikes[m]["dias"][d]['greves'][strike.company] = []
        strikes[m]["dias"][d]['greves'][strike.company].append(strike)


    m = datetime.today().strftime("%m")
    if len(strikes) > 0 and strikes.has_key(m):
        fix = False
        if strikes[m]["dias"].has_key(amanha):
            strikes[m]["dias"][amanha]["alias"] = "Amanhã"
            fix = True        

        if strikes[m]["dias"].has_key(hoje):
            strikes[m]["dias"][hoje]["alias"] = "Hoje"
            if fix:
                strikes[m]["dias"][hoje]["fix"] = "fixAmanha"
            for c in strikes[m]["dias"][hoje]["greves"]:
                cc = strikes[m]["dias"][hoje]["greves"][c]
                if len(cc) > 1:
                    strikes[m]["dias"][hoje]["greves"][c] = sorted(cc, key=MYattrgetter('start_date.day'), reverse=True)

    
    #strikes['04']["dias"] = sorted(strikes['04']["dias"])


    context = { 'strikes': strikes, 'regions': regions, 'host': request.get_host(), 'companies': companies, 'highlights': [int(highlight)] }
    
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
