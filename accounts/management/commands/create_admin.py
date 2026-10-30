from getpass import getpass

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email


class Command(BaseCommand):
	help = 'Create an admin superuser for the custom user model.'

	def handle(self, *args, **options):
		user_model = get_user_model()
		email = input('Email address: ').strip().lower()
		try:
			validate_email(email)
		except ValidationError as error:
			raise CommandError('; '.join(error.messages)) from error

		phone_number = input('Phone number: ').strip()
		if not phone_number:
			raise CommandError('Phone number is required.')
		if user_model.objects.filter(email__iexact=email).exists():
			raise CommandError('A user with that email address already exists.')
		if user_model.objects.filter(phone_number=phone_number).exists():
			raise CommandError('A user with that phone number already exists.')

		password = getpass('Password: ')
		confirmation = getpass('Password (again): ')
		if password != confirmation:
			raise CommandError('The passwords did not match.')

		candidate = user_model(email=email, phone_number=phone_number, role='admin')
		try:
			validate_password(password, candidate)
		except ValidationError as error:
			raise CommandError('; '.join(error.messages)) from error

		user = user_model.objects.create_superuser(
			email=email,
			phone_number=phone_number,
			password=password,
			role='admin',
		)
		self.stdout.write(self.style.SUCCESS(f'Superuser {user.email} created successfully.'))
