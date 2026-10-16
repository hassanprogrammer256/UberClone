from django.http import request
from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.generic import View,TemplateView
from .forms import LoginForm,CustomerForm
from  django.contrib.auth import authenticate, login

class RegisterView(TemplateView):
    template_name = 'auth/register.html'
    form_class = CustomerForm

    def get(self, request):
            form = self.form_class
            return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == 'POST':
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
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('index')

                else:
                    messages.error(request, 'Invalid username or password.')
        messages.error(request, 'Invalid username or password.')

        return render(request, 'auth/login.html',context={'form': form, 'error_message': 'Invalid username or password.'})



    
