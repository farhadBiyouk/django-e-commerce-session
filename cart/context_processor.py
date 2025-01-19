from cart.cart import Cart


def show_count(request):
	return {'cart_count': Cart(request)}
