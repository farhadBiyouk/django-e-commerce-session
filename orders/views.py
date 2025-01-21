from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from orders.forms import CreateOrderForm
from orders.models import OrderItem
from orders.tasks import notify_create_order
from cart.cart import Cart


@login_required
def create_order(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = CreateOrderForm(request.POST)
		if form.is_valid():
			order = form.save()
			request.session['order_id'] = order.id
			for item in cart:
				OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'],
				                         user_id=request.user.id,
				                         price=item['price'])
				
				cart.clear()
				
				notify_create_order.delay(order.id)
				return render(request, 'order/complete_order.html', {'order': order})
	else:
		form = CreateOrderForm()
	return render(request, 'order/create_order.html', {'form': form, 'cart': cart})
