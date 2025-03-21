from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomerForm
from django.contrib import messages
from .models import Membership
from .forms import MembershipForm


# Create your views here.
def join_up(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for joining up! A member of staff will contact you within 24hrs.")
            return redirect('join_up:join_up')

    else:
        form = CustomerForm()

    return render(request, 'join_up/join_up.html', {'form': form, 'join_up_messages': messages.get_messages(request)})


def membership_list(request):
    memberships = Membership.objects.filter(active=True)
    return render(request, 'join_up/memberships.html', {'memberships': memberships})


def superuser_required(function=None):
    return user_passes_test(lambda u: u.is_superuser)(function)


@superuser_required
def manage_memberships(request):
    memberships = Membership.objects.all()
    return render(request, 'join_up/manage_memberships.html', {'memberships': memberships})


@superuser_required
def edit_membership(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)

    if request.method == "POST":
        form = MembershipForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            return redirect('join_up:manage_memberships')

    else:
        form = MembershipForm(instance=membership)

    return render(request, 'join_up/edit_membership.html', {'form': form})


def delete_membership(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)

    if request.method == "POST":
        membership.delete()
        messages.success(request, "Membership deleted successfully.")
        return redirect('join_up:manage_memberships')

    messages.error(request, "Invalid request method.")
    return redirect('join_up:manage_memberships')


def superuser_required(function=None):
    return user_passes_test(lambda u: u.is_superuser)(function)


@superuser_required
def create_membership(request):
    if request.method == "POST":
        form = MembershipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('join_up:manage_memberships')
    else:
        form = MembershipForm()
    return render(request, 'join_up/create_membership.html', {'form': form})
