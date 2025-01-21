from django.shortcuts import render, redirect
from django.urls import reverse

from orders.forms import CreateOrderForm
from orders.models import OrderItem
from orders.tasks import notify_create_order
from cart.cart import Cart


def create_order(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = CreateOrderForm(request.POST)
		if form.is_valid():
			order = form.save()
			request.session['order_id'] = order.id
			for item in cart:
				OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'],
				                         price=item['price'])
			
			cart.clear()
			
			notify_create_order.delay(order.id)
			return redirect(reverse('zarinpal:request'))
	else:
		form = CreateOrderForm()
	return render(request, 'order/create_order.html', {'form': form, 'cart': cart})
