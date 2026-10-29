from django.contrib import admin
from django.urls import include, path
from .views import HomePageView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', HomePageView, name='index'),
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('manager/', include('manager.urls')),
    path('api/', include('api.urls'))
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)