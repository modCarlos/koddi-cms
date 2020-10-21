from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from page.models import Tag, Category, Course, Post, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from wp_admin.forms import CourseForm, PostForm, CategoryForm, TagForm, UserForm, UserProfileForm
import re, string, random, datetime
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.auth import login as auth_login

@staff_member_required
def index(request):
	context_dict = {}
	categories = Category.objects.all()
	profiles = UserProfile.objects.all()
	posts = Post.objects.all()
	tags = Tag.objects.all()
	courses = Course.objects.all()

	context_dict['categories'] = categories
	context_dict['profiles'] = profiles
	context_dict['posts'] = posts
	context_dict['tags'] = tags
	context_dict['courses'] = courses
	context_dict['profile'] = UserProfile.objects.get(user=request.user)

	return render(request,'wp-admin/index.html',context_dict)

@staff_member_required
def courses(request):
	context_dict = {}
	courses = Course.objects.all()

	for course in courses:
		course.posts = Post.objects.filter(course=course).count()

	context_dict['courses'] = courses
	context_dict['profile'] = UserProfile.objects.get(user=request.user)

	return render(request,'wp-admin/courses.html',context_dict)

@staff_member_required
def posts(request):
	context_dict = {}
	posts = Post.objects.all()

	context_dict['posts'] = posts
	context_dict['profile'] = UserProfile.objects.get(user=request.user)

	return render(request,'wp-admin/posts.html',context_dict)

@staff_member_required
def tags(request):
	context_dict = {}
	tags = Tag.objects.all()
	for tag in tags:
		tag.posts = Post.objects.filter(tags=tag).count()

	context_dict['tags'] = tags
	context_dict['profile'] = UserProfile.objects.get(user=request.user)
	return render(request,'wp-admin/tags.html',context_dict)

@staff_member_required
def users(request):
	context_dict = {}
	users = UserProfile.objects.all()
	for user in users:
		user.posts = Post.objects.filter(author=user.user).count()

	context_dict['users'] = users
	context_dict['profile'] = UserProfile.objects.get(user=request.user)
	return render(request,'wp-admin/users.html',context_dict)

@staff_member_required
def categories(request):
	context_dict = {}
	categories = Category.objects.all()
	for category in categories:
		category.courses = Course.objects.filter(category=category).count()
		category.posts = Post.objects.filter(category=category).count()

	context_dict['categories'] = categories
	context_dict['profile'] = UserProfile.objects.get(user=request.user)

	return render(request,'wp-admin/categories.html',context_dict)

@staff_member_required
def statistics(request):
	context_dict = {}
	
	context_dict['profile'] = UserProfile.objects.get(user=request.user)
	return render(request,'wp-admin/statistics.html',context_dict)

@staff_member_required
def settings(request):
	context_dict = {}
	context_dict['profile'] = UserProfile.objects.get(user=request.user)
	return render(request,'wp-admin/settings.html',context_dict)

@staff_member_required
def payments(request):
	context_dict = {}
	context_dict['profile'] = UserProfile.objects.get(user=request.user)
	return render(request,'wp-admin/payments.html',context_dict)

@staff_member_required
def add_course(request):
	context_dict = {}
	context_dict['profile'] = UserProfile.objects.get(user=request.user)

	if request.method == 'POST':
		form = CourseForm(request.POST, request.FILES)
		if form.is_valid():
			course = form.save(commit=False)
			course.author = request.user

			if 'wall' in request.FILES:
				course.wall = request.FILES['wall']

			course.save()

			return HttpResponseRedirect('/kd-admin/courses/')
		else:
			print form.errors

	form = CourseForm(initial={'author':User.objects.get(username='josept')})
	context_dict['form'] = form

	return render(request,'wp-admin/add_course.html',context_dict)

@staff_member_required
def add_post(request):
	context_dict = {}
	context_dict['profile'] = UserProfile.objects.get(user=request.user)

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user

			if 'wall' in request.FILES:
				post.wall = request.FILES['wall']

			post.save()
			form.save_m2m()

			return HttpResponseRedirect('/kd-admin/posts/')
		else:
			print form.errors

	form = PostForm(initial={'author':User.objects.get(username='josept')})
	context_dict['form'] = form

	return render(request,'wp-admin/add_post.html',context_dict)

@staff_member_required
def add_category(request):
	context_dict = {}
	context_dict['profile'] = UserProfile.objects.get(user=request.user)

	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect('/kd-admin/categories/')
		else:
			print form.errors

	form = CategoryForm()
	context_dict['form'] = form
	return render(request,'wp-admin/add_category.html',context_dict)

@staff_member_required
def add_tag(request):
	context_dict = {}
	context_dict['profile'] = UserProfile.objects.get(user=request.user)

	if request.method == 'POST':
		form = TagForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect('/kd-admin/tags/')
		else:
			print form.errors

	form = TagForm()
	context_dict['form'] = form
	return render(request,'wp-admin/add_tag.html',context_dict)

@staff_member_required
def add_superuser(request):
	context_dict = {}
	context_dict['profile'] = UserProfile.objects.get(user=request.user)

	if request.method == 'POST':
		form = UserForm(data = request.POST)
		profile_form = UserProfileForm(request.POST, request.FILES)
		if form.is_valid() and profile_form.is_valid():
			user = form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'image' in request.FILES:
				profile.image = request.FILES['image']
			profile.save()
			return HttpResponseRedirect('/kd-admin/users/')
		else:
			print form.errors, profile_form.errors

	form = UserForm()
	profile_form = UserProfileForm()
	context_dict['form'] = form
	context_dict['profile_form'] = profile_form

	return render(request,'wp-admin/add_superuser.html',context_dict)

@staff_member_required
def edit_course(request,slug):
	context_dict = {}
	context_dict['profile'] = UserProfile.objects.get(user=request.user)
	course = get_object_or_404(Course,slug=slug)
	context_dict['course'] = course

	if request.method == 'POST':
		form = CourseForm(request.POST, request.FILES, instance=course)
		if form.is_valid():
			course = form.save(commit=False)

			if 'wall' in request.FILES:
				course.wall = request.FILES['wall']

			course.save()

			return HttpResponseRedirect('/kd-admin/courses/')
		else:
			print form.errors

	form = CourseForm(instance=course)
	context_dict['form'] = form

	return render(request,'wp-admin/edit_course.html',context_dict)

@staff_member_required
def edit_post(request,slug):
	context_dict = {}
	context_dict['profile'] = UserProfile.objects.get(user=request.user)
	post = get_object_or_404(Post,slug=slug)
	context_dict['post'] = post

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			post = form.save(commit=False)

			if 'wall' in request.FILES:
				post.wall = request.FILES['wall']

			post.save()
			form.save_m2m()

			return HttpResponseRedirect('/kd-admin/posts/')
		else:
			print form.errors

	form = PostForm(instance=post)
	context_dict['form'] = form

	return render(request,'wp-admin/edit_post.html',context_dict)

@staff_member_required
def edit_category(request,slug):
	context_dict = {}
	context_dict['profile'] = UserProfile.objects.get(user=request.user)
	category = get_object_or_404(Category,slug=slug)

	if request.method == 'POST':
		form = CategoryForm(request.POST, instance=category)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect('/kd-admin/categories/')
		else:
			print form.errors

	form = CategoryForm(instance=category)
	context_dict['form'] = form
	return render(request,'wp-admin/edit_category.html',context_dict)

@staff_member_required
def edit_tag(request,slug):
	context_dict = {}
	context_dict['profile'] = UserProfile.objects.get(user=request.user)
	tag = get_object_or_404(Tag,slug=slug)

	if request.method == 'POST':
		form = TagForm(request.POST, instance=tag)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect('/kd-admin/tags/')
		else:
			print form.errors

	form = TagForm(instance=tag)
	context_dict['form'] = form
	return render(request,'wp-admin/edit_tag.html',context_dict)


@staff_member_required
def edit_user(request,slug):
	context_dict = {}
	context_dict['profile'] = UserProfile.objects.get(user=request.user)
	user = get_object_or_404(User, username=slug)
	profile = get_object_or_404(UserProfile, user=user)

	if request.method == 'POST':
		form = UserForm(data = request.POST, instance=user)
		profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid() and profile_form.is_valid():
			user = form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'image' in request.FILES:
				profile.image = request.FILES['image']
			profile.save()
			return HttpResponseRedirect('/wp-admin/users/')
		else:
			print form.errors, profile_form.errors

	form = UserForm(instance=user)
	profile_form = UserProfileForm(instance=profile)
	context_dict['form'] = form
	context_dict['profile_form'] = profile_form

	return render(request,'wp-admin/edit_superuser.html',context_dict)

@staff_member_required
def del_course(request,slug):
	get_object_or_404(Course,slug=slug).delete()
	return HttpResponseRedirect('/kd-admin/courses/')

@staff_member_required
def del_post(request,slug):
	get_object_or_404(Post,slug=slug).delete()
	return HttpResponseRedirect('/kd-admin/posts/')

@staff_member_required
def del_category(request,slug):
	get_object_or_404(Category,slug=slug).delete()
	return HttpResponseRedirect('/kd-admin/categories/')

@staff_member_required
def del_tag(request,slug):
	get_object_or_404(Tag,slug=slug).delete()
	return HttpResponseRedirect('/kd-admin/tags/')
