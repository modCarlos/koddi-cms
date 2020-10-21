from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters
from decimal import Decimal
from payments import PurchasedItem
from payments.models import BasePayment

# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length=128)
	slug = models.SlugField(max_length=128)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = defaultfilters.slugify(self.name)
		super(Tag, self).save(*args, **kwargs)


class Category(models.Model):
	name = models.CharField(max_length=128)
	slug = models.SlugField(max_length=128)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = defaultfilters.slugify(self.name)
		super(Category, self).save(*args, **kwargs)


class Course(models.Model):
	name = models.CharField(max_length=128)
	slug = models.SlugField(max_length=128)
	description = models.TextField()
	created_at = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=False)
	author = models.ForeignKey(User,null=True,blank=True,related_name='author_course')
	wall = models.ImageField(upload_to='wall_images')
	category = models.ForeignKey(Category,null=True,related_name='category_course')

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = defaultfilters.slugify(self.name)
		super(Course, self).save(*args, **kwargs)

class Post(models.Model):
	name = models.CharField(max_length=128)
	slug = models.SlugField(max_length=128)
	summary = models.CharField(max_length=240)
	content = models.TextField()
	repository = models.URLField(blank=True)
	course = models.ForeignKey(Course,blank=True,null=True,related_name='course_post')
	author = models.ForeignKey(User,related_name='author')
	position = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now=True)
	wall = models.ImageField(upload_to='wall_images')
	tags = models.ManyToManyField(Tag,related_name='tags_post')
	category = models.ForeignKey(Category,null=True,related_name='category_post')

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = defaultfilters.slugify(self.name)
		super(Post, self).save(*args, **kwargs)

class UserProfile(models.Model):
	user = models.OneToOneField(User,related_name='user')
	description = models.TextField()
	twitter = models.CharField(max_length=128,blank=True)
	facebook = models.CharField(max_length=128,blank=True)
	google_plus = models.CharField(max_length=128,blank=True)
	image = models.ImageField(upload_to='image')
	favorites = models.ManyToManyField(Post,related_name='favorites')

	#FAcebook
	facebook_uid = models.PositiveIntegerField(blank=True, null=True)
	facebook_access_token = models.CharField(blank=True, max_length=255)
	facebook_access_token_expires = models.PositiveIntegerField(blank=True, null=True)

	#cart
	#cart = models.ManyToManyField(Post,related_name='cart')

	def __unicode__(self):
		return self.user.username

"""
	Cart Section
"""
class Cart(models.Model):
	user = models.OneToOneField(User, related_name='user_cart')

	def __unicode__(self):
		return self.user.username

class Article(models.Model):
	post = models.ForeignKey(Post,related_name='article')
	quantity = models.PositiveIntegerField(default=0)
	cart = models.ForeignKey(Cart, related_name='cart')

	def __unicode__(self):
		return self.post.name

"""
	Payments section
"""
class Payment(BasePayment):

    def get_failure_url(self):
        return 'http://example.com/failure/'

    def get_success_url(self):
        return 'http://example.com/success/'

    def get_purchased_items(self):
        # you'll probably want to retrieve these from an associated order
        yield PurchasedItem(name='The Hound of the Baskervilles', sku='BSKV',
                            quantity=9, price=Decimal(10), currency='USD')
