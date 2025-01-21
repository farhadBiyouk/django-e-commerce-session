from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils import timezone


from coupon.forms import CouponForm
from coupon.models import Coupon


@require_POST
def apply_coupon(request):
	now = timezone.now()
	form = CouponForm(request.POST)
	if form.is_valid():
		try:
			coupon = Coupon.objects.get(code__exact=form.cleaned_data['code'])
			request.session['coupon_id'] = coupon.id
		except:
			request.session['coupon_id'] = None
		
	return redirect(reverse('cart:cart-detail'))