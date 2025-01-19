from django.urls import path

from shop import views

app_name = 'shop'
urlpatterns = [
	path('', views.product_list, name='product-list'),
	path('<category_slug>/', views.product_list, name='product-list-category'),
	path('<int:id>/<slug>/', views.product_detail, name='product-detail'),
]
