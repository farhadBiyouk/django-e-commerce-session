from django.urls import path
from coupon import views

app_name = 'coupon'
urlpatterns = [
	path('apply/', views.apply_coupon, name='coupon-apply')
]
