from django.contrib import admin
from page.models import Post, Course, Tag, Category, UserProfile, Payment
# Register your models here.
admin.site.register(Post)
admin.site.register(Course)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Payment)