from django.urls import path
from . import views

app_name = 'staff_panel'

urlpatterns = [
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('delete/<int:customer_id>/', views.delete_join_request, name='delete_join_request'),
    path('user-admin/', views.user_admin, name='user_admin'),
    path('create-user/', views.create_user, name='create_user'),
    path('promote-to-staff/<int:user_id>/', views.promote_to_staff, name='promote_to_staff'),
    path('toggle-active/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),
    path('update-user/<int:user_id>/', views.update_user_settings, name='update_user_settings'),
    path('reset-password/<int:user_id>/', views.reset_password, name='reset_password'),
    path('closed-days/', views.closed_day_list, name='closed_day_list'),
    path('add-closed-day/', views.add_closed_day, name='add_closed_day'),
    path('delete-closed-day/<int:pk>/', views.delete_closed_day, name='delete_closed_day'),
]
