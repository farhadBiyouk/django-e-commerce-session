from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from orders.forms import CreateOrderForm
from orders.models import OrderItem, Order
from orders.tasks import notify_create_order
from cart.cart import Cart


@staff_member_required
def admin_order_detail(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	return render(request,
'admin/orders/order/detail.html',{'order': order})

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
