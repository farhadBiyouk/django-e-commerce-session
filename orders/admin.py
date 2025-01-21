import csv

from django.contrib import admin
from django.http import HttpResponse

from orders.models import Order, OrderItem, Product

from datetime import datetime


def export_to_csv(modeladmin, request, queryset):
	opts = modeladmin.model._meta
	content_disposition = f'attachment; filename={opts.verbose_name}.csv'
	response = HttpResponse(content_type='text/csv')
	response['Content_Disposition'] = content_disposition
	writer = csv.writer(response)
	
	fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
	
	writer.writerow([field.verbose_name for field in fields])
	
	for obj in queryset:
		data_row = []
		for field in fields:
			value = getattr(obj, field.name)
			if isinstance(value, datetime):
				value = value.strftime('%d/%m/%Y')
			data_row.append(value)
		writer.writerow(data_row)
	return response

export_to_csv.short_description = 'Export to CSV'



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
	actions = [export_to_csv]
