from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
	confirm_password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'enter confirm password'}))
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for key, field in self.fields.items():
			field.label = ""
			field.help_text = ""
	
	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'confirm_password']
		widgets = {
			'username': forms.TextInput(
				attrs={'class': 'form-control', 'placeholder': 'enter username', }),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'enter email address'}),
			'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'enter password'}),
		}
	
	def clean_confirm_password_(self):
		password1 = self.cleaned_data['password']
		password2 = self.cleaned_data['confirm_password']
		
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('password not match')
		return password1


class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput())
