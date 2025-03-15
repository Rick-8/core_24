from django.urls import path
from . import views
from .views import memberships_list

urlpatterns = [
    path('', views.join_up, name='join_up'),
    path('memberships/', memberships_list, name='memberships'),
]
