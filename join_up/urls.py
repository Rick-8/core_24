from django.urls import path, include
from . import views


app_name = 'join_up'

urlpatterns = [
    path('', views.join_up, name='join_up'),
    path('memberships/', views.membership_list, name='memberships'),
    path('manage-memberships/', views.manage_memberships, name='manage_memberships'),
    path('create-membership/', views.create_membership, name='create_membership'),
    path('memberships/edit/<int:membership_id>/', views.edit_membership, name='edit_membership'),
    path('memberships/delete/<int:membership_id>/', views.delete_membership, name='delete_membership'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
