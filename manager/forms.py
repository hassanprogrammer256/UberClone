from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from accounts.models import GENDER_CHOICES
from accounts.models import DriverProfile
from api.models import CustomerPayment, Trip


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


class DriverAdminForm(forms.Form):
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
	date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
	address = forms.CharField(max_length=500)

	def __init__(self, *args, driver=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.driver = driver
		if driver and not self.is_bound:
			self.initial = {
				'first_name': driver.user.first_name,
				'last_name': driver.user.last_name,
				'phone_number': driver.user.phone_number,
				'email': driver.user.email,
				'gender': driver.user.gender,
				'date_of_birth': driver.date_of_birth,
				'address': driver.address,
			}

	def clean_email(self):
		email = self.cleaned_data['email'].strip().lower()
		users = get_user_model().objects.filter(email__iexact=email)
		if self.driver:
			users = users.exclude(pk=self.driver.user_id)
		if users.exists():
			raise ValidationError('An account with this email already exists.')
		return email

	def clean_phone_number(self):
		phone_number = self.cleaned_data['phone_number'].strip()
		users = get_user_model().objects.filter(phone_number=phone_number)
		if self.driver:
			users = users.exclude(pk=self.driver.user_id)
		if users.exists():
			raise ValidationError('An account with this phone number already exists.')
		return phone_number


class TripAdminForm(forms.ModelForm):
	class Meta:
		model = Trip
		fields = ('customer', 'driver', 'vehicle', 'origin', 'destination', 'trip_date', 'requested_at', 'status')
		widgets = {
			'trip_date': forms.DateInput(attrs={'type': 'date'}),
			'requested_at': forms.TimeInput(attrs={'type': 'time'}),
		}

class CustomerPaymentAdminForm(forms.ModelForm):
	class Meta:
		model = CustomerPayment
		fields = ('customer', 'trip', 'amount', 'payment_method', 'payment_date', 'payment_time')
		widgets = {
			'payment_date': forms.DateInput(attrs={'type': 'date'}),
			'payment_time': forms.TimeInput(attrs={'type': 'time'}),
		}