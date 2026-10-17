from django.urls import path
from .views import RegisterView,LoginView, auth_view


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('get-started/', auth_view, name='auth')
]