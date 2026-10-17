from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Customer, CustomUser, Driver

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'image']

class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = ['image','username', 'email', 'first_name', 'last_name', 'phone_number', 'password']

class CustomerForm(ModelForm):
    username = forms.CharField(required=False, widget=forms.HiddenInput)
    terms = forms.BooleanField(required=True)
    marketing = forms.BooleanField(required=False)
    confirm_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'accept': 'image/jpeg,image/png,image/webp',
            'class': 'auth-avatar-input',
            'aria-label': 'Choose a profile photo',
            'aria-hidden': 'true',
            'tabindex': '-1',
        })

    class Meta:
        model = Customer
        fields = ['image', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'password', 'confirm_password', 'terms', 'marketing']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '')
        username = cleaned_data.get('username', '').strip()

        if not username and email:
            username = email.split('@', 1)[0]
            base_username = username
            suffix = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f'{base_username}{suffix}'
                suffix += 1
            cleaned_data['username'] = username

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data['password']
        if not any(character.isdigit() for character in password):
            raise forms.ValidationError('Include at least one number.')
        if not any(not character.isalnum() for character in password):
            raise forms.ValidationError('Include at least one symbol.')
        try:
            validate_password(password, self.instance)
        except ValidationError as error:
            raise forms.ValidationError(error.messages) from error
        return password

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.set_password(self.cleaned_data['password'])
        if commit:
            customer.save()
        return customer

class LoginForm(AuthenticationForm):
    def clean_username(self):
        identifier = self.cleaned_data['username'].strip()
        user = CustomUser.objects.filter(username=identifier).first()

        if user is None and '@' in identifier:
            email_matches = list(CustomUser.objects.filter(email__iexact=identifier)[:2])
            if len(email_matches) == 1:
                user = email_matches[0]

        if user is None:
            phone_matches = list(
                CustomUser.objects.filter(phone_number__in=self._phone_candidates(identifier))[:2]
            )
            if len(phone_matches) == 1:
                user = phone_matches[0]

        return user.get_username() if user is not None else identifier

    @staticmethod
    def _phone_candidates(identifier):
        digits = ''.join(character for character in identifier if character.isdigit())
        if digits.startswith('00'):
            digits = digits[2:]

        local_digits = digits[3:] if digits.startswith('256') else digits
        if local_digits.startswith('0'):
            local_digits = local_digits[1:]

        candidates = {identifier, digits}
        if local_digits:
            candidates.update({
                f'0{local_digits}',
                f'256{local_digits}',
                f'+256{local_digits}',
            })
        return candidates

    class Meta:
        model = CustomUser  
        fields = ['username', 'password']
