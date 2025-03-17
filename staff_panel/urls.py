from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from . import views

app_name = 'staff_panel'


urlpatterns = [
    path('staff_dashboard/', staff_member_required(views.staff_dashboard), name='staff_dashboard'),
    path('delete_join_request/<int:customer_id>/', staff_member_required(views.delete_join_request), name='delete_join_request'),
    path('user_admin/', staff_member_required(views.user_admin), name='user_admin'),
    path('create_user/', staff_member_required(views.create_user), name='create_user'),
    path('toggle_user_active/<int:user_id>/', staff_member_required(views.toggle_user_active), name='toggle_user_active'),
    path('reset_password/<int:user_id>/', staff_member_required(views.reset_password), name='reset_password'),
    path('closed_days/', staff_member_required(views.closed_day_list), name='closed_day_list'),
    path('add_closed_day/', staff_member_required(views.add_closed_day), name='add_closed_day'),
    path('delete_closed_day/<int:pk>/', staff_member_required(views.delete_closed_day), name='delete_closed_day'),

    # Superuser-only URLs
    path('promote_to_staff/<int:user_id>/', views.promote_to_staff, name='promote_to_staff'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update_user/<int:user_id>/', views.update_user_settings, name='update_user_settings'),
]
