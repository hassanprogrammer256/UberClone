from django.urls import path
from .views import auth_view, RegisterView, LoginView
from django.contrib.auth.views import LogoutView    



urlpatterns = [
    path('auth/', auth_view, name='auth'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView, name='register'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout')

]