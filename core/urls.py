from django.contrib import admin
from django.urls import include, path
from .views import HomePageView

urlpatterns = [
    path('', HomePageView, name='index'),
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('manager/', include('manager.urls')),
    path('api/', include('api.urls'))
]
