from django import forms

from orders.models import Order


class CreateOrderForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for key, field in self.fields.items():
			field.label = ""
	
	class Meta:
		model = Order
		fields = ['first_name', 'last_name', 'email', 'address', 'city', 'postal_code']
		widgets = {
			'first_name': forms.TextInput(
				attrs={'class': 'form-control', 'placeholder': 'enter first name', }),
			'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter last name'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'enter email address'}),
			'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'enter address'}),
			'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter city',}),
			'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter ZIP Code'}),
		}
