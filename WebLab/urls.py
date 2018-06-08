from django.conf.urls import url, include
from django.contrib import admin
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.Index, name='index'),
    url(r'^profile', views.profile, name='prof'),
    url(r'^login/', include('logins.urls')),
    url(r'^post/', include('Posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)