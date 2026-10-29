from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from accounts.models import GENDER_CHOICES


class CustomerAdminForm(forms.Form):
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	phone_number = forms.CharField(max_length=15)
	email = forms.EmailField()
	gender = forms.ChoiceField(
		choices=[('', 'Select gender'), *GENDER_CHOICES], required=False
	)
	image = forms.ImageField(
		required=False,
		widget=forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/png,image/webp'}),
	)
	address = forms.CharField(widget=forms.Textarea, max_length=500)

	def __init__(self, *args, customer=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.customer = customer
		if customer and not args and not kwargs.get('data'):
			self.initial = {
				'first_name': customer.user.first_name,
				'last_name': customer.user.last_name,
				'phone_number': customer.user.phone_number,
				'email': customer.user.email,
				'gender': customer.user.gender,
				'address': customer.address,
			}

	def clean_email(self):
		email = self.cleaned_data['email'].strip().lower()
		users = get_user_model().objects.filter(email__iexact=email)
		if self.customer:
			users = users.exclude(pk=self.customer.user_id)
		if users.exists():
			raise ValidationError('An account with this email already exists.')
		return email

	def clean_phone_number(self):
		phone_number = self.cleaned_data['phone_number'].strip()
		users = get_user_model().objects.filter(phone_number=phone_number)
		if self.customer:
			users = users.exclude(pk=self.customer.user_id)
		if users.exists():
			raise ValidationError('An account with this phone number already exists.')
		return phone_number