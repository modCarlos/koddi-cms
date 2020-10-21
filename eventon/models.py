from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters
from django.utils.translation import ugettext as _
from tastypie.models import create_api_key
# Create your models here.

class Ecategory(models.Model):
	name = models.CharField(max_length=128)
	photo = models.ImageField(upload_to='categories',null=True)
	slug = models.SlugField(max_length=128)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = defaultfilters.slugify(self.name)
		super(Ecategory, self).save(*args, **kwargs)

class Etag(models.Model):
	name = models.CharField(max_length=128)
	slug = models.SlugField(max_length=128)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = defaultfilters.slugify(self.name)
		super(Etag, self).save(*args, **kwargs)

class Eplace(models.Model):
	name = models.CharField(max_length=128)
	address = models.CharField(max_length=256)
	location = models.CharField(max_length=20)
	photo = models.ImageField(upload_to='places')
	slug = models.SlugField(max_length=128)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = defaultfilters.slugify(self.name)
		super(Eplace, self).save(*args, **kwargs)

class Eevent(models.Model):
	name = models.CharField(max_length=128)
	slug = models.SlugField(max_length=128)
	photo = models.ImageField(upload_to='events',null=True)
	date = models.DateField()
	description = models.TextField(blank=True)
	place = models.ForeignKey(Eplace,null=True)
	category = models.ForeignKey(Ecategory)

	def save(self, *args, **kwargs):
		self.slug = defaultfilters.slugify(self.name)
		super(Eevent, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class Epost(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=128)
	description = models.TextField()
	num_tickets = models.IntegerField(default=0)
	event = models.ForeignKey(Eevent,null=True)
	slug = models.SlugField(max_length=128)
	price = models.FloatField(default=0)
	active = models.BooleanField(default=False)
	tags = models.ManyToManyField(Etag)
	photo = models.ImageField(upload_to='posts',null=True)

	def save(self, *args, **kwargs):
		self.slug = defaultfilters.slugify(self.name)
		super(Epost, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class Etransaction(models.Model):
	from_user = models.ForeignKey(User,related_name='from_user')
	to_user = models.ForeignKey(User,related_name='to_user')
	date = models.DateField(auto_now=True)
	post = models.ForeignKey(Epost)
	rating = models.IntegerField(default=0)

	def __unicode__(self):
		return self.from_user.username

class EuserProfile(models.Model):
	user = models.OneToOneField(User)
	description = models.TextField()
	seller = models.BooleanField(default=False)
	#image = models.ImageField(upload_to='image')
	wishlist = models.ManyToManyField(Epost)
	rating = models.IntegerField(default=0)
	seller_date = models.DateField(null=True)

	facebook_uid = models.PositiveIntegerField(blank=True, null=True)
	facebook_access_token = models.CharField(blank=True, max_length=255)
	facebook_access_token_expires = models.PositiveIntegerField(blank=True, null=True)

	def __unicode__(self):
		return self.user.username

class Ecomment(models.Model):
	user = models.ForeignKey(User)
	comment = models.TextField()
	#if response ?
	response = models.BooleanField(default=False)
	comment_response = models.ForeignKey('self')

	date = models.DateTimeField(auto_now=True)
	post = models.ForeignKey(Epost)

	def __unicode__(self):
		return self.user.username
#Comments powered by facebook?
#blog? is it important?

models.signals.post_save.connect(create_api_key, sender=User)
