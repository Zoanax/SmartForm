from django.shortcuts import render, redirect
from .forms import UserForm


def form_view(request):
    return render(request, "smartform/form.html")


def user_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_created')
    else:
        form = UserForm()
    return render(request, 'smartform/user_form.html', {'form': form})


def user_created(request):
    return render(request, 'smartform/user_created.html')
