from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Choice

class UserSignupForm(UserCreationForm):

	email = forms.EmailField()
	fname = forms.CharField(max_length=50, label='First Name')
	lname = forms.CharField(max_length=50, label='Last Name')
	anonymous = forms.BooleanField(required=False, label='Keep me Anonymous')

	class Meta:
		model = User
		fields = ['username', 'fname', 'lname', 'email', 'password1', 'password2', 'anonymous']


class CreatePollForm(forms.Form):

	question_text = forms.CharField(max_length=200,
			widget=forms.Textarea(attrs={'id': 'question_string', 'rows':3, 'placeholder': 'Question Text'}),
			error_messages={'required': 'Please Enter Question Text.'},
			required=True)
	choice1 = forms.CharField(max_length=100,
			widget=forms.TextInput(attrs={'id': 'choice1_string', 'placeholder': 'Enter Choice 1'}),
			error_messages={'required': 'You have to enter atleast two choices.'},
			required=True)
	choice2 = forms.CharField(max_length=100,
			widget=forms.TextInput(attrs={'id': 'choice2_string', 'placeholder': 'Enter Choice 2'}),
			error_messages={'required': 'You have to enter atleast two choices.'},
			required=True)
	choice3 = forms.CharField(max_length=100,
			widget=forms.TextInput(attrs={'id': 'choice3_string', 'placeholder': 'Enter Choice 3 (optional)'}),
			required=False)
	choice4 = forms.CharField(max_length=100,
			widget=forms.TextInput(attrs={'id': 'choice4_string', 'placeholder': 'Enter Choice 4 (optional)'}),
			required=False)
	choice5 = forms.CharField(max_length=100,
			widget=forms.TextInput(attrs={'id': 'choice5_string', 'placeholder': 'Enter Choice 5 (optional)'}),
			required=False)


class UserUpdateForm(forms.ModelForm):

	email = forms.EmailField()
	fname = forms.CharField(max_length=50, label='First Name')
	lname = forms.CharField(max_length=50, label='Last Name')
	anonymous = forms.BooleanField(required=False, label='Keep me Anonymous')

	class Meta:
		model = User
		fields = ['username', 'fname', 'lname', 'email', 'anonymous']

