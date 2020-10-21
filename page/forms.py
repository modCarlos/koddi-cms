from django import forms
from django.contrib.auth.models import User
from page.models import UserProfile

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
		fields = ('description', 'image')