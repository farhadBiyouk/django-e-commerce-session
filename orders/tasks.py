from celery import shared_task

from django.core.mail import send_mail

from orders.models import Order


@shared_task
def notify_create_order(order_id):
	order = Order.objects.get(id=order_id)
	subject = f'created number {order.id}'
	message = f'Dear {order.first_name} your order is ready'
	sent_mail = send_mail(subject, message, 'admin@admin.com', [order.email])
	return sent_mail
