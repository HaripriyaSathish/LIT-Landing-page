from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from core.views import home, info_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('<slug:slug>/', info_page, name='info_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
