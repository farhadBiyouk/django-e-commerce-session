from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
	path('register/', views.signup, name='register'),
	path('login/', views.signin, name='login'),
	path('logout/', views.logout_user, name='logout'),
]
