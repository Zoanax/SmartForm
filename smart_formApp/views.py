from django.shortcuts import render, redirect

from scheduler.tasks_scheduler import task_send_welcome_email
from .forms import UserForm
from .models import User



def form_view(request):
    return render(request, "smartform/form.html")


# def user_form(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             if send_it(request,user.email,user.first_name,user.last_name):
#                 user.welcome_email=True
#                 user.save()
#                 return redirect('user_created')
#             else:
#                 print("Email was not sent")
#     else:
#         form = UserForm()
#     return render(request, 'smartform/user_form.html', {'form': form})


def user_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Check if email already exists in database
            if User.objects.filter(email=user.email).exists():
                #send_it(request, user.email, user.first_name, user.last_name)
                task_send_welcome_email(user.email, user.first_name, user.last_name,f"Welcome_email"+user.email)
                print("Email already exists")
                return redirect('user_created')  # redirect to a different page, or display an error message
            else:
                # If email does not exist, send the welcome email and save the user to database
                if task_send_welcome_email(user.email, user.first_name, user.last_name,f"Welcome_email"+user.email):
                    user.welcome_email = True
                    user.save()
                    print("Email Sent views.py")
                    return redirect('user_created')
                else:
                    print("Email was not sent")
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
