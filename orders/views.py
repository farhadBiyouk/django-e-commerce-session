from django.shortcuts import render, redirect

from orders.forms import CreateOrderForm
from orders.models import OrderItem
from cart.cart import Cart


def create_order(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = CreateOrderForm(request.POST)
		if form.is_valid():
			order = form.save()
			for item in cart:
				OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'],
				                         price=item['price'])
			
			cart.clear()
			return render(request, 'order/complete_order.html', {'order': order})
	else:
		form = CreateOrderForm()
	return render(request, 'order/create_order.html', {'form': form, 'cart': cart})
