# coding=utf-8
from models import Strike, Region, Company
from forms import SubmitForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import SortedDict
from django.template import RequestContext
import locale
from datetime import datetime, date, timedelta

locale.setlocale(locale.LC_ALL, "pt_PT.UTF-8")


def index(request, highlight=''):
    latest_strikes = Strike.objects.filter(end_date__gte=datetime.today().date()).order_by('start_date')[:10]
    companies = Company.objects.all()
    regions = Region.objects.all()
    
    strikes = SortedDict()
    
    hoje = datetime.today().strftime("%d")
    amanha = datetime.today().date() + timedelta(days=1)
    amanha = amanha.strftime("%d")

    for strike in latest_strikes:
        m = strike.start_date.strftime("%m")
        d = strike.start_date.strftime("%d")
        
        if strike.start_date < datetime.today():
            d = hoje
        
        if not strikes.has_key(m):
            strikes[m] = {"nome":strike.start_date.strftime("%B"), "dias":SortedDict()}
        if not strikes[m]["dias"].has_key(d):
            strikes[m]["dias"][d] = {'greves':{}}
        if not strikes[m]["dias"][d]['greves'].has_key(strike.company):
            strikes[m]["dias"][d]['greves'][strike.company] = []
        strikes[m]["dias"][d]['greves'][strike.company].append(strike)

    if len(strikes) > 0:
        fix = False
        if strikes[m]["dias"].has_key(amanha):
            strikes[m]["dias"][amanha]["alias"] = "Amanhã"
            fix = True        

        if strikes[m]["dias"].has_key(hoje):
            strikes[m]["dias"][hoje]["alias"] = "Hoje"
            if fix:
                strikes[m]["dias"][hoje]["fix"] = "fixAmanha"

    
    #strikes['04']["dias"] = sorted(strikes['04']["dias"])

    context = { 'strikes': strikes, 'regions': regions, 'host': request.get_host(), 'companies': companies }
    
    return render_to_response('index.html', context)

	if highlight == '':
	    highlight = '-1'

	context = { 'strikes': strikes, 'regions': regions, 'host': request.get_host(), 'companies': companies, 'highlights': [int(highlight)] }
	return render_to_response('index.html', context)
	

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
        
@login_required
@csrf_protect
def submit(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/thanks')
    else:
        form = SubmitForm()

    return render_to_response('submit.html', { 'form': form }, context_instance=RequestContext(request))
    
def submissions(request):
    latest_strikes = Strike.objects.filter(start_date__gte=datetime.today().date()).order_by('start_date')
    companies = Company.objects.all()
    regions = Region.objects.all()
    
    strikes = SortedDict()
    
    hoje = datetime.today().strftime("%d")
    amanha = datetime.today().date() + timedelta(days=1)
    amanha = amanha.strftime("%d")

    for strike in latest_strikes:
        m = strike.start_date.strftime("%m")
        d = strike.start_date.strftime("%d")
        
        if not strikes.has_key(m):
            strikes[m] = {"nome":strike.start_date.strftime("%B"), "dias":SortedDict()}
        if not strikes[m]["dias"].has_key(d):
            strikes[m]["dias"][d] = {'greves':{}}
        if not strikes[m]["dias"][d]['greves'].has_key(strike.company):
            strikes[m]["dias"][d]['greves'][strike.company] = []
        strikes[m]["dias"][d]['greves'][strike.company].append(strike)

    if len(strikes) > 0:
        fix = False
        if strikes[m]["dias"].has_key(amanha):
            strikes[m]["dias"][amanha]["alias"] = "Amanhã"
            fix = True        

        if strikes[m]["dias"].has_key(hoje):
            strikes[m]["dias"][hoje]["alias"] = "Hoje"
            if fix:
                strikes[m]["dias"][hoje]["fix"] = "fixAmanha"

    
    #strikes['04']["dias"] = sorted(strikes['04']["dias"])


    context = { 'strikes': strikes, 'regions': regions, 'host': request.get_host(), 'companies': companies }
    
    return render_to_response('submissions.html', context)

def login(request):
    return render_to_response('login.html')