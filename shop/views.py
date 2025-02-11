from django.shortcuts import render, get_object_or_404

from shop.models import Category, Product
from shop.recommendation import Recommender
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
	category = None
	categories = Category.objects.all()
	products = Product.objects.filter(available=True)
	
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
	context = {
		'category': category,
		'categories': categories,
		'products': products
	}
	return render(request, 'shop/product_list.html', context)


def product_detail(request, id, slug):
	product = get_object_or_404(Product, id=id, slug=slug)
	r = Recommender()
	recommender_product = r.suggest_product_for([product], 2)
	form = CartAddProductForm()
	return render(request, 'shop/product_detail.html',
	              {'product': product, 'form': form, 'recommender_product': recommender_product})
