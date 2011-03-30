from hat.models import Strike, Region
#from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.http import HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

def index(request):
	latest_strikes = Strike.objects.filter(start_date__gte=datetime.now()).order_by('-start_date')[:10]
	regions = Region.objects.all()
	context = { 'strikes': latest_strikes, 'regions': regions, 'host': request.get_host() }
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