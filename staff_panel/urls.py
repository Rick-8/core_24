from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from . import views


app_name = 'staff_panel'


urlpatterns = [
    # Staff-only accessible paths
    path('staff-dashboard/', staff_member_required(views.staff_dashboard), name='staff_dashboard'),
    path('delete-join-request/<int:customer_id>/', staff_member_required(views.delete_join_request), name='delete_join_request'),
    path('user-admin/', staff_member_required(views.user_admin), name='user_admin'),
    path('create-user/', staff_member_required(views.create_user), name='create_user'),
    path('toggle-user-active/<int:user_id>/', staff_member_required(views.toggle_user_active), name='toggle_user_active'),
    path('reset-password/<int:user_id>/', staff_member_required(views.reset_password), name='reset_password'),
    path('closed-days/', staff_member_required(views.closed_day_list), name='closed_day_list'),
    path('add-closed-day/', staff_member_required(views.add_closed_day), name='add_closed_day'),
    path('delete-closed-day/<int:pk>/', staff_member_required(views.delete_closed_day), name='delete_closed_day'),

    # Superuser-only URLs
    path('promote-to-staff/<int:user_id>/', views.promote_to_staff, name='promote_to_staff'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update-user/<int:user_id>/', views.update_user_settings, name='update_user_settings'),
]
