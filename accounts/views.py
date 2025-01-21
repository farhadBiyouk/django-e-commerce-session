from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from accounts.forms import RegisterForm, LoginForm


def signup(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			if User.objects.filter(username=form.cleaned_data['username']).exists():
				return redirect(reverse('accounts:register'))
			new_user = form.save(commit=False)
			new_user.set_password(form.cleaned_data['password'])
			new_user.save()
			return redirect(reverse('accounts:login'))
	else:
		form = RegisterForm()
	return render(request, 'accounts/register.html', {'form': form})


def signin(reqeust):
	if reqeust.method == 'POST':
		form = LoginForm(reqeust.POST)
		if form.is_valid():
			user = authenticate(reqeust, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			if user is not None:
				login(reqeust, user)
				return redirect(reverse('shop:product-list'))
			else:
				return redirect(reverse('accounts:register'))
	else:
		form = LoginForm()
	return render(reqeust, 'accounts/login.html', {'form': form})


@login_required
def logout_user(request):
	logout(request)
	return redirect(reverse('shop:product-list'))
