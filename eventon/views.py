from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import re, string, random, datetime
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.auth import login as auth_login
from models import Ecategory, Etag, Epost, Eevent, EuserProfile, Etransaction, Ecomment
import httplib2
import urllib
from django.conf import settings
import json as simplejson
from models import EuserProfile

#search
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

# Create your views here.
def index(request):
	context_dict = {}
	events = Eevent.objects.all().order_by('-date')[:4]
	context_dict['events'] = events

	return render(render,'event-on/index.html',context_dict)

def events(request):
	context_dict = {}
	events = Eevent.objects.all()

	paginator = Paginator(events, 15)
	try:
		page = int(request.GET.get("page", '1'))
	except ValueError:
		page = 1

	try:
		events = paginator.page(page)
	except (InvalidPage, EmptyPage):
		events = paginator.page(paginator.num_pages)

	context_dict['events'] = events
	return render(request,'event-on/events.html',context_dict)

def event(request,slug):
	context_dict = {}
	event = get_object_or_404(Eevent, slug=slug)
	posts = Epost.objects.filter(event=event)

	paginator = Paginator(posts, 15)
	try:
		page = int(request.GET.get("page", '1'))
	except ValueError:
		page = 1

	try:
		posts = paginator.page(page)
	except (InvalidPage, EmptyPage):
		posts = paginator.page(paginator.num_pages)

	context_dict['posts'] = posts
	context_dict['event'] = event

	return render(request,'event-on/event.html',context_dict)

def categories(request):
	context_dict = {}
	categories = Ecategory.objects.all()
	context_dict['categories'] = categories

	return render(request,'event-on/categories.html',context_dict)

def category(request,slug):
	context_dict = {}
	category = get_object_or_404(Ecategory, slug=slug)
	events = Eevent.objects.filter(category=category)

	paginator = Paginator(events, 15)
	try:
		page = int(request.GET.get("page", '1'))
	except ValueError:
		page = 1

	try:
		events = paginator.page(page)
	except (InvalidPage, EmptyPage):
		events = paginator.page(paginator.num_pages)

	context_dict['category'] = category
	context_dict['events'] = events

	return render(request,'event-on/category.html',context_dict)

def calendar(request):
	context_dict = {}

	events = Eevent.objects.filter(date__gt=datetime.date.today()).order_by('-date')
	context_dict['events'] = events

	return render(request,'event-on/calendar.html',context_dict)

def post(request,slug):
	context_dict = {}
	post = get_object_or_404(Epost,slug=slug)

	context_dict['post'] = post
	return render(request,'event-on/post.html',context_dict)

def tag(request,slug):
	context_dict = {}
	tag = get_object_or_404(Etag, slug=slug)
	posts = Post.objects.filter(tags=tag)

	paginator = Paginator(posts, 15)
	try:
		page = int(request.GET.get("page", '1'))
	except ValueError:
		page = 1

	try:
		posts = paginator.page(page)
	except (InvalidPage, EmptyPage):
		posts = paginator.page(paginator.num_pages)

	context_dict['tag'] = tag
	context_dict['posts'] = posts

	return render(request,'event-on/tag.html',context_dict)

@login_required
def profile(request):
	context_dict = {}

	profile = get_object_or_404(EuserProfile, user=request.user)
	context_dict['profile'] = profile

	return render(request,'event-on/profile.html',context_dict)

@login_required
def edit_profile(request):
	context_dict = {}

	return render(request,'event-on/edit_profile.html',context_dict)

@login_required
def wishlist(request):
	context_dict = {}

	profile = get_object_or_404(EuserProfile, user=request.user)
	context_dict['profile'] = profile

	return render('event-on/wishlist.html',context_dict)

@login_required
def boughts(request):
	context_dict = {}

	boughts = Etransaction.objects.filter(to_user=request.user)
	profile = get_object_or_404(EuserProfile, user=request.user)
	context_dict['boughts'] = boughts
	context_dict['profile'] = profile

	return render(request,'event-on/boughts.html',context_dict)

@login_required
def upgrade(request):
	context_dict = {}

	#Upgrade account and connect with paypal
	profile = get_object_or_404(EuserProfile, user=request.user)
	context_dict['profile'] = profile

	return HttpResponseRedirect('/event-on/')

@login_required
def buy_ticket(request,slug):
	context_dict = {}
	#post = Epost.objects.get(slug=slug)
	post = get_object_or_404(Epost, slug=slug)
	context_dict['post'] = post

	return render(request,'event-on/buy_ticket.html',context_dict)

def login(request):
	context_dict = {}

	if request.method == 'POST':
		if request.POST['username'] and request.POST['password']:
			username = request.POST['username']
			password = request.POST['password']

			user = authenticate(username=username, password=password)
			if user:
				auth_login(request, user)
				return HttpResponseRedirect('/event-on/')
		else:
			print 'Incorrect Data'
	else:
		print 'No method post'

	return render(request,'event-on/login.html',context_dict)

def register(request):
	context_dict = {}

	#form = UserForm()
	#profileForm = ProfileForm()

	if request.method == 'POST':
		pass
		#if form.is_valid() and profileForm.is_valid():
		#	pass

		#	login 

		#	return HttpResponseRedirect('/event-on/')

	return render(request,'event-on/register.html',context_dict)

def logout(request):

	return HttpResponseRedirect('/event-on/')

def search(request):
	context_dict = {}

	# search
	query_string = ''
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']
		entry_query = get_query(query_string, ['name'])

		results = Epost.objects.filter(entry_query)
		paginator = Paginator(results, 15)
		try:
			page = int(request.GET.get("page", '1'))
		except ValueError:
			page = 1

		try:
			results = paginator.page(page)
		except (InvalidPage, EmptyPage):
			results = paginator.page(paginator.num_pages)
		context_dict['results'] = results

	context_dict['search'] = query_string

	return render(request,'event-on/search.html',context_dict)

@login_required
def create_post(request):
	context_dict = {}

	if request.method == 'POST':
		pass

	return render(request,'event-on/create_post.html',context_dict)

@login_required
def add_to_wishlist(request):
	context_dict = {}

	profile = get_object_or_404(EuserProfile, user=request.user)
	post = get_object_or_404(Epost, slug=request.GET['post'])
	profile.wishlist.add(post)
	profile.save()

	return HttpResponse('Done')

def comment(request):
	context_dict = {}

	comment, created = Ecomment.objects.get_or_create(user=request.user, comment=request.GET['comment'])

	return HttpResponse('Commented')

def facebook(request):
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': 'http://localhost:8080/event-on/facebook/',
        'client_secret': settings.FACEBOOK_SECRET_KEY,
        'code': request.GET['code']
    }

    http = httplib2.Http(timeout=15)
    response, content = http.request('https://graph.facebook.com/oauth/access_token?%s' % urllib.urlencode(params))
    
    # Find access token and expire (this is really gross)
    params = content.split('&')
    ACCESS_TOKEN = params[0].split('=')[1]
    EXPIRE = params[1].split('=')[1]
    
    # Get basic information about the person
    response, content = http.request('https://graph.facebook.com/me?access_token=%s' % ACCESS_TOKEN)
    response_email = content_email = http.request('https://graph.facebook.com/me?access_token%s' % ACCESS_TOKEN)
    data = json.loads(content)
    data_email = json.loads(content_email)
    
    # Try to find existing profile, create a new user if one doesn't exist
    try:
        profile = EuserProfile.objects.get(facebook_uid=data['id'])
        #user = authenticate(username=data['id'], password=data[id])
        #return HttpResponseRedirect('/')
    except EuserProfile.DoesNotExist:
        user = User.objects.create_user(data['username'], data['email'], data['id'], first_name=data['first_name'], last_name=data['last_name'])
        profile, created = EuserProfile.objects.get_or_create(user=user)
        profile.facebook_uid = data['id']
    
    # Update token and expire fields on profile
    profile.facebook_access_token = ACCESS_TOKEN
    profile.facebook_access_token_expires = EXPIRE
    profile.save()
    
    # Authenticate and log user in
    user = authenticate(username=profile.user.username, password=profile.facebook_uid)
    login(request, user)
    
    return HttpResponseRedirect('/event-on/')

def reset(request):
	return password_reset(request, template_name='reset.html',
        email_template_name='reset_email.html',
        subject_template_name='reset_subject.txt',
        post_reset_redirect=reverse('success'))

def reset_confirm(request, uidb64=None, token=None):
	return password_reset_confirm(request, template_name='reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('success'))

def success(request):
	return render(request, "success.html")