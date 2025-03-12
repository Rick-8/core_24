from django.urls import path
from . import views  # Import the views to handle the routes
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.book_slot, name='book_slot'),
    path('confirmation/<int:booking_id>/', views.confirmation, name='confirmation'),
    path('logged_out/', views.logged_out, name='logged_out'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
