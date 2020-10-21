from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect

def active_cart(f):
	def wrap(request, *args, **kwargs):
		if settings.USE_CART:
			return f(request, *args, **kwargs)
		else:
			return HttpResponseRedirect('/')
	return wrap