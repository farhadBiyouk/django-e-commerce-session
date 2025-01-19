from django.contrib import admin

from orders.models import Order, OrderItem, Product


class OrderItemAdmin(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ('product',)
	extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'created', 'updated',
	                'paid']
	list_filter = ['created', 'updated', 'paid']
	inlines = [OrderItemAdmin]
