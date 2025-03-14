from django.shortcuts import render


# Create your views here.
from django.shortcuts import render, redirect
from .forms import CustomerForm
from django.contrib import messages


def join_up(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for joining up!\nA member of staff will contact you soon.")
            return redirect('join_up')
    else:
        form = CustomerForm()

    return render(request, 'join_up/join_up.html', {'form': form})
