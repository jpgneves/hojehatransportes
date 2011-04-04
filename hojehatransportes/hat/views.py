# coding=utf-8
from models import Strike, Region, Company
#from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import SortedDict
import locale
from datetime import datetime, date

locale.setlocale(locale.LC_ALL, "pt_PT.UTF-8")

def index(request):
	latest_strikes = Strike.objects.filter(start_date__gte=datetime.today().date()).order_by('start_date')[:10]
	companies = Company.objects.all()
	regions = Region.objects.all()
	
	strikes = {}
	
	for strike in latest_strikes:
		m = strike.start_date.strftime("%m")
		d = strike.start_date.strftime("%d")
		
		if not strikes.has_key(m):
			strikes[m] = {"nome":strike.start_date.strftime("%B"), "dias":SortedDict()}
		if not strikes[m]["dias"].has_key(d):
			strikes[m]["dias"][d] = {}
		if not strikes[m]["dias"][d].has_key(strike.company):
			strikes[m]["dias"][d][strike.company] = []
		strikes[m]["dias"][d][strike.company].append(strike)
	
	#strikes['04']["dias"] = sorted(strikes['04']["dias"])


	context = { 'strikes': strikes, 'regions': regions, 'host': request.get_host(), 'companies': companies }
	
	#alterar
	#context['statichost']="localhost/~carlos/hojehatransportes/hojehatransportes/static"
	context['statichost']="static.hagreve.com"
	
	return render_to_response('index.html', context)

@require_POST
def submit(request):
	pass

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
