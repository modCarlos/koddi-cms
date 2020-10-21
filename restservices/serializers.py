from django.forms import widgets
from rest_framework import serializers
from page.models import Post, Tag, Category, Course, UserProfile#, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
	author = serializers.HyperlinkedRelatedField(read_only=True,view_name='user-detail')

	class Meta:
		model = Post
		fields = ('name','slug','summary','author','wall')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username','author')

class TagSerializer(serializers.HyperlinkedModelSerializer):
	tags = serializers.HyperlinkedRelatedField(many=True, view_name='tag-detail', read_only=True)

	class Meta:
		model = Tag
		fields = ('name','tags')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
	category_post = serializers.HyperlinkedRelatedField(many=True, view_name='category-detail', read_only=True)

	class Meta:
		model = Tag
		fields = ('name','category_post')

class CourseSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Course
		fields = ('name',)

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
	user = serializers.ReadOnlyField(source='user.username')
	class Meta:
		model = UserProfile
		fields = ('description','user')