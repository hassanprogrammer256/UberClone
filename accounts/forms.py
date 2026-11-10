from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError

from api.models import Location


class RegistrationForm(forms.Form):
	role = forms.ChoiceField(
		choices=(('customer', 'Customer'), ('driver', 'Driver')),
		widget=forms.HiddenInput(),
	)
	first_name = forms.CharField(
		max_length=30,
		widget=forms.TextInput(attrs={
			'class': 'uber-field',
			'autocomplete': 'given-name',
			'required': True,
		}),
	)
	last_name = forms.CharField(
		max_length=30,
		widget=forms.TextInput(attrs={
			'class': 'uber-field',
			'autocomplete': 'family-name',
			'required': True,
		}),
	)
	email = forms.EmailField(
		widget=forms.EmailInput(attrs={
			'class': 'uber-field',
			'autocomplete': 'email',
			'required': True,
		}),
	)
	phone_number = forms.CharField(
		max_length=15,
		widget=forms.TelInput(attrs={
			'class': 'uber-field',
			'autocomplete': 'tel',
			'required': True,
		}),
	)
	date_of_birth = forms.DateField(
		widget=forms.DateInput(attrs={
			'class': 'uber-field',
			'type': 'date',
			'autocomplete': 'bday',
			'required': True,
		}),
	)
	image = forms.ImageField(
		required=False,
		widget=forms.ClearableFileInput(attrs={
			'class': 'auth-avatar-input',
			'accept': 'image/jpeg,image/png,image/webp',
		}),
	)
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={
			'class': 'uber-field',
			'autocomplete': 'new-password',
			'required': True,
		}),
	)
	confirm_password = forms.CharField(
		widget=forms.PasswordInput(attrs={
			'class': 'uber-field',
			'autocomplete': 'new-password',
			'required': True,
		}),
	)
	location = forms.ModelChoiceField(
		queryset=Location.objects.all(),
		empty_label='Select a location',
		widget=forms.Select(attrs={'class': 'uber-field'}),
	)
	terms = forms.BooleanField(required=True)
	marketing = forms.BooleanField(required=False)

	def __init__(self, *args, role='customer', **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['role'].initial = role
		self.fields['date_of_birth'].required = role == 'driver'

    

	def clean_email(self):
		email = self.cleaned_data['email'].strip().lower()
		if get_user_model().objects.filter(email__iexact=email).exists():
			raise ValidationError('An account with this email address already exists.')
		return email

	def clean_phone_number(self):
		phone_number = self.cleaned_data['phone_number'].strip()
		if get_user_model().objects.filter(phone_number=phone_number).exists():
			raise ValidationError('An account with this phone number already exists.')
		return phone_number

	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')

		if password and confirm_password and password != confirm_password:
			self.add_error('confirm_password', 'Passwords do not match.')
		if password:
			try:
				password_validation.validate_password(password)
			except ValidationError as error:
				self.add_error('password', error)

		return cleaned_data

	