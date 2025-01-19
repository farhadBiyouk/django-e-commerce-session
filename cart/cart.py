from django.conf import settings

from shop.models import Product


class Cart:
	"""
	initial basket for user
	"""
	
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(settings.SESSION_CART_ID)
		if not cart:
			cart = self.session[settings.SESSION_CART_ID] = {}
		self.cart = cart
	
	def add(self, product, quantity=1, override_quantity=False):
		"""
		added new product to basket if product was added just update quantity
		"""
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity': 0, 'price': int(product.price)}
		if override_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity
		
		self.save()
	
	def remove(self, product):
		"""
		remove product from basket
		
		"""
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()
	
	def __iter__(self):
		"""
		added additional info to basket and computing total price for each product
		
		"""
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		cart = self.cart.copy()
		
		for product in products:
			cart[str(product.id)]['product'] = product
		
		for item in cart.values():
			item['total_price'] = item['quantity'] * int(item['price'])
			yield item
	
	def __len__(self):
		"""
		take quantity basket
	
		"""
		return sum(item['quantity'] for item in self.cart.values())
	
	def get_total_price(self):
		"""
		take total price basket
		
		"""
		return sum(item['quantity'] * int(item['price']) for item in self.cart.values())
	
	def save(self):
		self.session.modified = True
	
	def clear(self):
		del self.session[settings.SESSION_CART_ID]
		self.save()
