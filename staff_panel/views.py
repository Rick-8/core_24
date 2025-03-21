from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from join_up.models import Customer
from bookings.models import ClosedDay
from .forms import ClosedDayForm, CustomUserCreationForm


def is_staff_user(user):
    return user.is_staff


def is_superuser(user):
    return user.is_superuser


@staff_member_required
def staff_dashboard(request):
    join_requests = Customer.objects.filter(status='pending')
    context = {'join_requests': join_requests}
    return render(request, 'staff_panel/staff_dashboard.html', context)


@staff_member_required
def delete_join_request(request, customer_id):
    if request.method == "POST":
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            messages.success(request, f'Join request for {customer.name} has been deleted.')
        except Customer.DoesNotExist:
            messages.error(request, 'The requested customer could not be found.')

    return redirect('staff_dashboard')


@staff_member_required
def user_admin(request):
    users = User.objects.all() if request.user.is_superuser else User.objects.filter(is_staff=False, is_superuser=False)
    return render(request, 'staff_panel/user_admin.html', {'users': users})


@staff_member_required
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect('staff_panel:user_admin')
        else:
            messages.error(request, "There was an error creating the user")
    else:
        form = CustomUserCreationForm()

    return render(request, 'staff_panel/create_user.html', {'form': form})


@staff_member_required
def toggle_user_active(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f'User {user.username} is now {"active" if user.is_active else "inactive"}.')
    return redirect('staff_panel:user_admin')


@user_passes_test(is_superuser, login_url='index')
def promote_to_staff(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if not user.is_staff:
            user.is_staff = True
            user.save()
            messages.success(request, f'User {user.username} has been promoted to staff.')
        else:
            messages.warning(request, f'User {user.username} is already a staff member.')
    except User.DoesNotExist:
        messages.error(request, 'The user could not be found.')

    return redirect('staff_panel:user_admin')


@user_passes_test(is_superuser, login_url='index')
def delete_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, "User deleted successfully.")
    return redirect("staff_panel:user_admin")


@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='index')
def update_user_settings(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        is_active = 'is_active' in request.POST
        is_staff = 'is_staff' in request.POST
        is_superuser = 'is_superuser' in request.POST

        if not username or not email:
            messages.error(request, "Username and Email are required.")
            return render(request, 'staff_panel/update_user_settings', {'user': user})

        user.username = username
        user.email = email
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        messages.success(request, f"User {user.username}'s settings have been updated successfully.")
        return redirect('staff_panel:user_admin')

    return render(request, 'staff_panel/update_user.html', {'user': user})


@staff_member_required
def reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Password reset successfully for {user.username}')
            return redirect('staff_panel:user_admin')
    else:
        form = SetPasswordForm(user)

    return render(request, 'staff_panel/reset_password.html', {'form': form, 'user': user})


@staff_member_required
def closed_day_list(request):
    closed_days = ClosedDay.objects.all()
    return render(request, 'staff_panel/closed_day_list.html', {'closed_days': closed_days})


@staff_member_required
def add_closed_day(request):
    if request.method == 'POST':
        form = ClosedDayForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Closed day added successfully.")
            return redirect('staff_panel:closed_day_list')
    else:
        form = ClosedDayForm()
    return render(request, 'staff_panel/add_closed_day.html', {'form': form})


@staff_member_required
def delete_closed_day(request, pk):
    try:
        closed_day = ClosedDay.objects.get(pk=pk)
        closed_day.delete()
        messages.success(request, "Closed day deleted successfully.")
    except ClosedDay.DoesNotExist:
        messages.error(request, "Closed day not found.")
    return redirect('staff_panel:closed_day_list')