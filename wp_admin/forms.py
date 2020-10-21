from django import forms
from django.contrib.auth.models import User
from page.models import Course, Category, Post, Tag, UserProfile
from ckeditor.widgets import CKEditorWidget

class CourseForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Course name")
	description = forms.CharField(widget = forms.Textarea, help_text="Course description")
	active = forms.BooleanField(help_text="Active")
	author = forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.HiddenInput())
	category = forms.ModelChoiceField(queryset=Category.objects.all(),help_text="Select category")
	wall = forms.FileField(
        label='Select image',
        help_text='Select image',
        required=False
    )

	class Meta:
		model = Course
		fields = ('name','description','active','wall','category','author')

class PostForm(forms.ModelForm):
	name = forms.CharField(max_length= 128, help_text="Post name")
	summary = forms.CharField(max_length= 240, help_text="Summary")
	content = forms.CharField(widget = forms.Textarea, help_text="Post content")
	repository = forms.URLField(help_text="URL repository",required=False)
	course = forms.ModelChoiceField(queryset=Course.objects.all(),help_text="Select course(Can be blank)", required=False)
	author = forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.HiddenInput())
	position = forms.IntegerField(help_text="Position (If course not null)",initial=0)
	wall = forms.FileField(
        label='Select image',
        help_text='Select image',
        required=False
    )
	#tags = models.ManyToManyField(Tag,null=True)
	category = forms.ModelChoiceField(queryset=Category.objects.all(),help_text="Select category")

	class Meta:
		model = Post
		fields = ('name','summary','repository','course','position','author','wall','category','tags','content')
		widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Category name")
	class Meta:
		model = Category
		fields = ('name',)

class TagForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Tag name")
	class Meta:
		model = Tag
		fields = ('name',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),help_text="Password")
    username = forms.CharField(max_length=30, help_text="Username (30 characters or fewer)")
    email = forms.EmailField(help_text="Email")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	description = forms.CharField(widget = forms.Textarea, help_text="Description")
	facebook = forms.CharField(max_length=128, help_text="Facebook link",required=False)
	twitter = forms.CharField(max_length=128, help_text="Twitter link",required=False)
	google_plus = forms.CharField(max_length=128, help_text="Google plus link",required=False)
	image = forms.FileField(
        label='Select image',
        help_text='Select image'
    )
	class Meta:
		model = UserProfile
		fields = ('description', 'facebook', 'twitter', 'google_plus', 'image')