from shop.models import Category


def show_category(request):
	return {'category_context': Category.objects.all()}
