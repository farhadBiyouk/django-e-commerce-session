from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse

from shop.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cart.add(product=product, quantity=form.cleaned_data['quantity'],
		         override_quantity=form.cleaned_data['override']
		         )
	
	return redirect('cart:cart-detail')


@require_POST
def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product=product)
	return redirect('cart:cart-detail')


def cart_detail(reqeust):
	cart = Cart(reqeust)
	for item in cart:
		item['update_quantity_form'] = CartAddProductForm(
			initial={
				'quantity': int(item['quantity']),
				'override': True
			}
		)
	return render(reqeust, 'cart/cart_detail.html', {'cart': cart})
