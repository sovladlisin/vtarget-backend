from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('think_bank.urls')),
    path('', include('users.urls')),
    path('', include('scheduler.urls')),
    path('', include('group_copy.urls')),
    path('', include('shutterstock.urls')),
    path('', include('utils.urls')),
    path('', include('charts.urls')),
    path('', include('chat.urls')),
    path('admin/', admin.site.urls),
    url(r'^files/', include('db_file_storage.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler404 = 'app.views.handler404'
