
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Administrador Move4it'

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/auth/', include(('api.users.router', 'users'), namespace='users')),
    path('api/', include(('api.move4it.router', 'move4it'), namespace='move4it')),
    path('api/password_reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
