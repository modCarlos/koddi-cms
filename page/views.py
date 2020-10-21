from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from page.models import Tag, Category, Course, Post, UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from page.forms import UserForm, UserProfileForm
import string, random, datetime, httplib2, urllib, hashlib
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.conf import settings
import json as simplejson
from django.db.models import Q
from django.template.response import TemplateResponse
from payments import get_payment_model, RedirectNeeded
from payments.forms import PaymentForm, CreditCardPaymentForm, CreditCardPaymentFormWithName
from decimal import Decimal
from celery_tasks import send_email_with_celery, send_mass_email_with_celery
from functions import get_query
from decorators import active_cart

"""
	Pages
"""

def index(request):
	context_dict = {}
	posts = Post.objects.all().order_by('-created_at')
	categories = Category.objects.all()
	paginator = Paginator(posts, 15)
	try:
		page = int(request.GET.get("page", '1'))
	except ValueError:
		page = 1

	try:
		posts = paginator.page(page)
	except (InvalidPage, EmptyPage):
		posts = paginator.page(paginator.num_pages)

	if request.user.is_authenticated():
		context_dict['profile'] = UserProfile.objects.get(user=request.user)

	context_dict['posts'] = posts
	context_dict['categories'] = categories

	return render(request,'index.html',context_dict)

def courses(request):
	context_dict = {}
	courses = Course.objects.all().order_by('-created_at')
	categories = Category.objects.all()
	paginator = Paginator(courses,15)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		courses = paginator.page(page)
	except (InvalidPage, EmptyPage):
		courses = paginator.page(paginator.num_pages)

	if request.user.is_authenticated():
		context_dict['profile'] = UserProfile.objects.get(user=request.user)

	context_dict['courses'] = courses
	context_dict['categories'] = categories

	return render(request,'courses.html', context_dict)

def category(request,slug_category):
	context_dict = {}
	category = get_object_or_404(Category, slug=slug_category) #Category.objects.get(slug=slug_category)
	categories = Category.objects.all()
	posts = Post.objects.filter(category=category).order_by('-created_at')
	paginator = Paginator(posts,15)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		posts = paginator.page(page)
	except (InvalidPage, EmptyPage):
		posts = paginator.page(paginator.num_pages)

	if request.user.is_authenticated():
		context_dict['profile'] = UserProfile.objects.get(user=request.user)

	context_dict['posts'] = posts
	context_dict['category'] = category
	context_dict['categories'] = categories

	return render(request,'category.html',context_dict)

def tutoriales(request):
	pass

def post(request,slug_post):
	context_dict = {}
	post = get_object_or_404(Post, slug=slug_post)
	categories = Category.objects.all()
	if request.user.is_authenticated():
		profile = get_object_or_404(UserProfile, user=request.user)
		context_dict['profile'] = profile
	author = UserProfile.objects.get(user=post.author)
	recent = Post.objects.all().order_by('-created_at')[:3]
	context_dict['post'] = post
	context_dict['recent'] = recent
	context_dict['categories'] = categories
	context_dict['author'] = author
	context_dict['use_cart'] = settings.USE_CART

	return render(request,'post.html',context_dict)

def course(request,slug_course):
	context_dict = {}
	try:
		course = get_object_or_404(Course, slug=slug_course)
		if request.user.is_authenticated():
			profile = UserProfile.objects.get(user=request.user)
			context_dict['profile'] = profile
		author = UserProfile.objects.get(user=course.author)
		categories = Category.objects.all()
		posts = Post.objects.filter(course=course).order_by('position')
		context_dict['course'] = course
		context_dict['posts'] = posts
		context_dict['categories'] = categories
		context_dict['author'] = author
	except Exception, e:
		context_dict['error'] = str(e)+ ' '+slug_course

	return render(request,'course.html',context_dict)

def tag(request,slug_tag):
	context_dict = {}
	tag = get_object_or_404(Tag, slug=slug_tag) #Tag.objects.get(slug=slug_tag)
	categories = Category.objects.all()
	posts = Post.objects.filter(tags=tag).order_by('created_at')

	paginator = Paginator(posts,15)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		posts = paginator.page(page)
	except (InvalidPage, EmptyPage):
		posts = paginator.page(paginator.num_pages)	

	if request.user.is_authenticated():
		context_dict['profile'] = UserProfile.objects.get(user=request.user)

	context_dict['tag'] = tag
	context_dict['posts'] = posts
	context_dict['categories'] = categories

	return render(request,'tag.html',context_dict)

def author(request,username):
	context_dict = {}
	author = get_object_or_404(User, username=username) #User.objects.get(username=username)
	categories = Category.objects.all()
	if request.user.is_authenticated():
		profile = UserProfile.objects.get(user=request.user)
		context_dict['profile'] = profile
	about = UserProfile.objects.get(user=author)
	num_posts = Post.objects.filter(author=author).count()
	context_dict['about'] = about
	context_dict['num_posts'] = num_posts
	context_dict['categories'] = categories

	return render(request,'author.html',context_dict) 

def author_posts(request,username):
	context_dict = {}
	author = get_object_or_404(User, username=username) #User.objects.get(username=username)
	profile = get_object_or_404(UserProfile, user=author) #UserProfile.objects.get(user=author)
	categories = Category.objects.all()
	num_posts = Post.objects.filter(author=author).count()
	posts = Post.objects.filter(author=author).order_by('-created_at')
	context_dict['profile'] = profile
	context_dict['num_posts'] = num_posts
	context_dict['posts'] = posts
	context_dict['categories'] = categories

	return render(request,'author_posts.html',context_dict) 

def login(request):
	context_dict = {}
	categories = Category.objects.all()
	if request.method == 'POST':
		if request.POST['username'] and request.POST['password']:
			username = request.POST['username']
			password = request.POST['password']

			user = authenticate(username=username, password=password)
			if user:
				auth_login(request, user)
				return HttpResponseRedirect('/')
		else:
			print 'Incorrect Data'
	else:
		print 'No method post'

	context_dict['categories'] = categories

	return render(request,'login.html',context_dict)

def register(request):
	categories = Category.objects.all()
	if request.method == 'POST':
		#Register here
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']

		user, created = User.objects.get_or_create(username=username,email=email)
		user.set_password(password)
		user.save()

		profile, created = UserProfile.objects.get_or_create(user=user)
		profile.save()

		user = authenticate(username=username, password=password)
		auth_login(request, user)
		"""form = UserForm(data=request.POST)
								profile_form = UserProfileForm(data=request.POST)
								if user_form.is_valid() and profile_form.is_valid():
									user = form.save()
									user.set_password(user.password)
									user.save()
									profile = profile_form.save(commit=False)
									profile.user = user
									if 'image' in request.FILES:
										profile.image = request.FILES['image']
						
									profile.save()"""
		return HttpResponseRedirect('/')
	else:
		pass
		#print form.errors, profile_form.errors

	form = UserForm()
	profile_form = UserProfileForm()

	return render(request,'register.html',{'form': form, 'profile_form': profile_form, 'categories': categories})

def change_password(request):
	if request.method == 'POST':
		if request.POST['password'] == request.POST['repeat-password']:
			request.user.set_password(request.POST['password'])
			request.user.save()
			return HttpResponseRedirect('/profile/')

	return render(request,'change_password.html')

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

def profile(request):
	context_dict = {}
	if request.user.is_authenticated():
		context_dict['profile'] = get_object_or_404(UserProfile, user=request.user) #UserProfile.objects.get(user=request.user)
	#context_dict['favorites'] = UserProfile.favorites.all()
	context_dict['categories'] = Category.objects.all()

	return render(request,'profile.html', context_dict)

def edit_profile(request):
	if request.user.is_authenticated():

		return render_to_response('edit.html')
	else:
		return HttpResponseRedirect('/auth/login/')

def contact(request):
	return render('contact.html')

def search(request):
	found_entries = {}
	categories = Category.objects.all()

	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']
		entry_query = get_query(query_string, ['name','content'])

		results = Post.objects.filter(entry_query).order_by('-created_at')
		paginator = Paginator(results, 15)
		try:
			page = int(request.GET.get("page", '1'))
		except ValueError:
			page = 1

		try:
			results = paginator.page(page)
		except (InvalidPage, EmptyPage):
			results = paginator.page(paginator.num_pages)
		found_entries['results'] = results

	found_entries['categories'] = categories

	if request.user.is_authenticated():
		found_entries['profile'] = UserProfile.objects.get(user=request.user)

	return render(request,'search.html',found_entries)

def about(request):
	context_dict = {}
	categories = Category.objects.all()

	if request.user.is_authenticated():
		context_dict['profile'] = UserProfile.objects.get(user=request.user)

	return render(request,'about.html',context_dict)

@login_required
def add_favorite(request):
	context_dict = {}

	profile = get_object_or_404(UserProfile, user=request.user)
	post = get_object_or_404(Post, slug=request.GET['post'])
	profile.favorites.add(post)
	profile.save()
	return HttpResponse('Added!')

@login_required
def remove_favorite(request):
	context_dict = {}

	profile = get_object_or_404(UserProfile, user=request.user)
	post = get_object_or_404(Post, slug=request.GET['post'])
	profile.favorites.remove(post)
	profile.save()
	return HttpResponse('Removed!')

"""
	Facebook Registration Section
"""
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

#Facebook
def facebook(request):
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': 'http://localhost:8080/facebook/',
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
    
    #Generate password with secret word in settings.py
    hash_object = hashlib.sha1(settings.SECRET_FB_KEY+data['id'])
    hex_dig = hash_object.hexdigest()

    # Try to find existing profile, create a new user if one doesn't exist
    try:
        profile = UserProfile.objects.get(facebook_uid=data['id'])
        #user = authenticate(username=data['id'], password=data[id])
        #return HttpResponseRedirect('/')
    except UserProfile.DoesNotExist:
        user = User.objects.create_user(data['id'], data['email'], hex_dig, first_name=data['first_name'], last_name=data['last_name'])
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.facebook_uid = data['id']
    
    # Update token and expire fields on profile
    profile.facebook_access_token = ACCESS_TOKEN
    profile.facebook_access_token_expires = EXPIRE
    profile.save()
    
    # Authenticate and log user in
    user = authenticate(username=profile.user.username, password=hex_dig)
    login(request, user)
    
    return HttpResponseRedirect('/')

"""
	Payment Section
"""
def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'payment.html',
                            {'form': form, 'payment': payment})

def checkout(request):
	form = CreditCardPaymentFormWithName()

	if request.POST:
		Payment = get_payment_model()
		payment = Payment.objects.create(
		    variant='default',  # this is the variant from PAYMENT_VARIANTS
		    description='',
		    total=Decimal(120),
		    tax=Decimal(20),
		    currency='MXN',
		    delivery=Decimal(10),
		    billing_first_name='Carlos',
		    billing_last_name='Fuentes',
		    billing_address_1='UNAM CU, Facultad de Ingenieria',
		    billing_address_2='',
		    billing_city='Mexico City',
		    billing_postcode='56617',
		    billing_country_code='MX',
		    billing_country_area='Mexico',
		    customer_ip_address='127.0.0.1')
		return redirect('/')

	return render(request,'payment.html',{'form':form})

def cart(request):
	return render(request,'cart.html')
