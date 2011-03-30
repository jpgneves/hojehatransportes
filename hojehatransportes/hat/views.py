from hat.models import Strike, Region
#from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
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
	pass
	
@require_POST
def downvote(request):
	pass