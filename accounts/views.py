from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate

def auth_view(request):
    return render(request, 'auth/auth.html')


def RegisterView(request):
    return render(request, 'auth/register.html')

class LoginView(TemplateView):
    template_name = 'auth/login.html'
    form_class = AuthenticationForm  
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user =  authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                role = getattr(user, 'role', None)
                print(f"User role: {role}") 
                if role == 'customer':
                    return redirect('customer_index')
                elif role == 'driver':
                    return redirect('driver_index')
                elif role == 'admin':
                    return redirect('administrator_index')
            return redirect('index') 
        else:
            return render(request, self.template_name, {'form': form})


    
def CustomerIndexView(request):
    return render(request, 'client/index.html')

def DriverIndexView(request):
    return render(request, 'driver/index.html')

def AdminIndexView(request):
    return render(request, 'administrator/index.html')