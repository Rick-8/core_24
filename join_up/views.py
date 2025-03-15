from django.shortcuts import render, redirect
from .forms import CustomerForm
from django.contrib import messages
from .models import Membership


# Create your views here.
def join_up(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Thank you for joining up!\nA member of staff will contact you soon.")
            return redirect('join_up')
    else:
        form = CustomerForm()

    return render(request, 'join_up/join_up.html', {'form': form})


def memberships_list(request):
    memberships = Membership.objects.all()
    return render(
        request, 'join_up/memberships.html', {'memberships': memberships})
