from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import CustomerForm, LoginForm
from django.contrib.auth import login

class RegisterView(TemplateView):
    template_name = 'auth/register.html'
    form_class = CustomerForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
        messages.error(request, 'Registration failed. Please correct the errors below.')
        return render(request, self.template_name, {'form': form})


class LoginView(TemplateView):
    template_name = 'auth/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class(request=request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Login successful!')
            return redirect('index')

        return render(
            request,
            self.template_name,
            {'form': form, 'error_message': 'Invalid username or password.'},
        )


def auth_view(request):
    return render(request, 'auth/auth.html')


    
