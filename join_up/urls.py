from django.urls import path
from . import views

urlpatterns = [
    path('', views.join_up, name='join_up'),
]
