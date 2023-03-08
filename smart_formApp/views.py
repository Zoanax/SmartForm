from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User


def form_view(request):
    return render(request, "smartform/form.html")


def user_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user_created')
    else:
        form = UserForm()
    return render(request, 'smartform/user_form.html', {'form': form})


def user_created(request):
    latest_user = User.objects.latest('created_at')
    context = {
        'first_name': latest_user.first_name,
        'last_name': latest_user.last_name,
    }
    return render(request, 'smartform/user_created.html', context=context)
