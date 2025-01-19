from django.urls import path

from orders import views

app_name = 'order'
urlpatterns = [
	path('create/', views.create_order, name='create-order'),
]