from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from chat.models import User
from chat.functions import *
import json
from django.utils import simplejson

def index(request):
	ret_list = get_google_links("miley")
	#counter = 0
	#for item in soup.find_all('li', class_='g'):
		# Get the title of the link (text shown on Google)
		
		# Get the final href of the link
	
	user_list = User.objects.order_by('-last_name')[:5]
	context = {'user_list': user_list, 'ret_list': ret_list}
	return render(request, 'chat/index.html', context)


def query(request):
	
	if request.is_ajax():
		try:
			ret_list = get_reddit()
		except KeyError:
			return HttpResponse('Error')
	else:
		ret_list = []
		raise Http404
	
	ret_val = json.dumps(ret_list)
	return HttpResponse(ret_val, content_type="application/json")


def chat(request):
	return render(request, 'chat/chat.html')
