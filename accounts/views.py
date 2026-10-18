from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme

def auth_view(request):
    return render(request, 'auth/auth.html')


def RegisterView(request):
    return render(request, 'auth/register.html')


class LoginView(TemplateView):
    template_name = 'auth/login.html'
    form_class = AuthenticationForm  
    redirect_authenticated_user = True

    def get_redirect_route_by_role(self, user):
        """Helper method to return the correct dashboard name based on user role."""
        role = getattr(user, 'role', None)
        if role == 'customer':
            return 'customer_index'
        elif role == 'driver':
            return 'driver_index'
        elif role == 'admin':
            return 'admin_index'
        return 'index'

    def dispatch(self, request, *args, **kwargs):
        # Handle `redirect_authenticated_user`: if they are already signed in,
        # skip the login page and kick them straight to their dashboard
        if self.redirect_authenticated_user and request.user.is_authenticated:
            return redirect(self.get_redirect_route_by_role(request.user))
            
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['next'] = self.request.GET.get('next', '')
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You are signed in.')
                
                next_url = request.POST.get('next') or request.GET.get('next')
                is_safe = url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure()
                )
                
                if next_url and is_safe:
                    return redirect(next_url)
                
                return redirect(self.get_redirect_route_by_role(user))
        
        messages.error(request, 'Sign-in failed. Check your phone number or email and password, then try again.')
        next_url = request.POST.get('next') or request.GET.get('next', '')
        return render(request, self.template_name, {'form': form, 'next': next_url})

