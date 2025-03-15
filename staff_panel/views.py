from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from join_up.models import Customer
from .forms import UserCreationForm, UserUpdateForm


@login_required
def staff_dashboard(request):
    if not request.user.is_staff:
        return redirect('index')

    # Get all join requests with a status of 'pending'
    join_requests = Customer.objects.filter(status='pending')

    # Pass the join requests to the template
    context = {
        'join_requests': join_requests,
    }

    return render(request, 'staff_panel/staff_dashboard.html', context)


@login_required
def delete_join_request(request, customer_id):
    if not request.user.is_staff:
        return redirect('index')

    if request.method == "POST":
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            messages.success(request, f'Join request for {customer.name} has been deleted.')
        except Customer.DoesNotExist:
            messages.error(request, 'The requested customer could not be found.')

    return redirect('staff_dashboard')


@login_required
def user_admin(request):
    if request.user.is_superuser:
        users = User.objects.all()
    else:
        users = User.objects.filter(is_staff=False, is_superuser=False)

    return render(request, 'staff_panel/user_admin.html', {'users': users})


def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Create the user
            messages.success(request, "User created successfully!")
            return redirect('user_admin')  # Redirect to user admin after creation
        else:
            messages.error(request, "There was an error creating the user")
    else:
        form = UserCreationForm()

    return render(request, 'staff_panel/create_user.html', {'form': form})


@login_required
def toggle_user_active(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to access this page.")

    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()

    messages.success(request, f'User {user.username} is now {"active" if user.is_active else "inactive"}.')
    return redirect('user_admin')


@login_required
def promote_to_staff(request, user_id):
    if not request.user.is_superuser:
        return redirect('index')

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

    return redirect('user_admin')


@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('index')

    user = get_object_or_404(User, id=user_id)
    user.delete()

    messages.success(request, f'User {user.username} has been deleted.')
    return redirect('user_admin')


@login_required
def update_user_settings(request, user_id):
    # Ensure only superusers can update user settings
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this page.")

    # Get the user object to be updated
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Update the user fields with the form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        is_active = 'is_active' in request.POST
        is_staff = 'is_staff' in request.POST
        is_superuser = 'is_superuser' in request.POST

        # Validate if username and email are not empty
        if not username or not email:
            messages.error(request, "Username and Email are required.")
            return render(request, 'staff_panel/update_user.html', {'user': user})

        # Update the user object
        user.username = username
        user.email = email
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        # Save the updated user object
        user.save()

        messages.success(request, f"User {user.username}'s settings have been updated successfully.")
        return redirect('user_admin')  # Redirect to the user admin page

    # For GET request, display the current user data in the form
    return render(request, 'staff_panel/update_user.html', {'user': user})


@login_required
def reset_password(request, user_id):
    if not request.user.is_staff:
        return redirect('index')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Password reset successfully for {user.username}')
            return redirect('user_admin')
    else:
        form = SetPasswordForm(user)

    return render(request, 'staff_panel/reset_password.html', {'form': form, 'user': user})
