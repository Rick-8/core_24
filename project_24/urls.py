from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from bookings.views import home, custom_logout, logged_out


urlpatterns = [
    path('', home, name='index'),
    path('admin/', admin.site.urls),
    path('join-up/', include('join_up.urls')),
    path('logout/', custom_logout, name='custom_logout'),
    path('accounts/', include('allauth.urls')),
    path('logged_out/', logged_out, name='logged_out'),
    path('bookings/', include('bookings.urls')),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
