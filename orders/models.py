from django.db import models

from shop.models import Product


class Order(models.Model):
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	email = models.EmailField(max_length=130, blank=True, null=True)
	address = models.TextField()
	postal_code = models.CharField(max_length=20)
	city = models.CharField(max_length=30)
	created = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now_add=True)
	paid = models.BooleanField(default=False)
	
	class Meta:
		ordering = ('-created',)
	
	def __str__(self):
		return f'order {self.first_name} {self.last_name}'
	
	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all)


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
	quantity = models.PositiveIntegerField(default=1)
	price = models.PositiveIntegerField()
	
	def __str__(self):
		return self.order.first_name
	
	def get_cost(self):
		return (self.quantity * int(self.price))
