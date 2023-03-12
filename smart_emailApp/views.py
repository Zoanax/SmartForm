from datetime import datetime, timedelta

from django.shortcuts import render, redirect

from SmartForm import settings
from smart_emailApp.forms import *
from smart_formApp.models import User


# Create your views here.

def home_view(request):
    members_count = User.objects.count()
    today = datetime.today()
    thirty_days_ago = today - timedelta(days=7)
    last7days = User.objects.filter(created_at__gte=thirty_days_ago).count()
    numberOf_scheduled_tasks = EmailTask.objects.filter(status="Scheduled").count()
    only_scheduled_tasks = EmailTask.objects.filter(status="Scheduled")
    # all_other_task = EmailTask.objects.filter(status="Not Scheduled")
    from django.db.models import Q
    not_scheduled_tasks = EmailTask.objects.filter(Q(status='Not Scheduled') | Q(status='Expired'))
    print(not_scheduled_tasks)

    context = {
        "members_count": members_count,
        "last7days":last7days,
        "numberOf_scheduled_tasks":numberOf_scheduled_tasks,
        'only_scheduled_tasks':only_scheduled_tasks,
        'not_scheduled_tasks':not_scheduled_tasks
    }

    return render(request, "smartemail/master_home.html", context)

def scheduled_email(request):
    context = {
        "email1": "",
        "email2": "",
    }
    return render(request, "smartemail/scheduled_email.html", context)

def create_email(request):
    form = CreateEmailForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            # handle_uploaded_file(request.FILES["Stage_image"])
            instance = form.save(commit=False)
            instance.save()
            return redirect('master_home')
        else:
            form =CreateEmailForm()
    context = {
        'form': form,
        'submit_btn': 'Create'

    }
    return render(request, 'smartemail/create.html', context)


def create_task(request):
    if request.method == 'POST':
        form = EmailTaskForm(request.POST, request.FILES)
        if form.is_valid():
            intance = form.save(commit=False)
            intance.status = 'Scheduled'
            intance.sender = settings.EMAIL_HOST_USER
            # if user left empty send email to all
            if not intance.recipients:
                members_list =[]
                all_memebers = User.objects.all()
                for member in all_memebers:
                    members_list.append(member.email)
                intance.recipients = members_list
            intance.save()
            return redirect('master_home')
            # Process the email task here
    else:
        form = EmailTaskForm()

    context = {
        'form': form,
        'submit_btn': 'Create'
    }
    return render(request, 'smartemail/create.html', context)


def edit_task(request, id):
    task = EmailTask.objects.get(id=id)
    form = EmailTaskForm(request.POST or None, instance=task)
    if form.is_valid():
        intance = form.save(commit=False)
        intance.status = 'Scheduled'
        intance.sender = settings.EMAIL_HOST_USER

        # if user left empty send email to all
        if not intance.recipients:
            members_list =[]
            all_memebers = User.objects.all()
            for member in all_memebers:
                members_list.append(member.email)
            intance.recipients = members_list

        intance.save()
        return redirect('master_home')
        # Process the email task here

    context = {
        'form': form,
        'submit_btn':'Update'

    }
    return render(request, 'smartemail/create.html', context)



def stop_task(request,id):

    members_count = User.objects.count()
    today = datetime.today()
    thirty_days_ago = today - timedelta(days=7)
    last7days = User.objects.filter(created_at__gte=thirty_days_ago).count()
    numberOf_scheduled_tasks = EmailTask.objects.filter(status="Scheduled").count()
    only_scheduled_tasks = EmailTask.objects.filter(status="Scheduled")
    from django.db.models import Q
    not_scheduled_tasks = EmailTask.objects.filter(Q(status='Not Scheduled') | Q(status='Expired'))
    context = {
        "members_count": members_count,
        "last7days":last7days,
        "numberOf_scheduled_tasks":numberOf_scheduled_tasks,
        'only_scheduled_tasks':only_scheduled_tasks,
        'not_scheduled_tasks':not_scheduled_tasks
    }
    EmailTask.objects.filter(id =id).update(status="Not Scheduled")
    return render(request, 'smartemail/master_home.html', context)


def email_view(request):
    emails = Emails.objects.all()
    context = {
        "emails":emails,
        'f_name':"John",
        "l_name":"Smith"
    }
    return render(request, "smartemail/emails.html", context)

def email_template_view(request,id):

    email = Emails.objects.filter(id=id)
    print(email)
    context = {
        "email_detail": email

    }

    return render(request, "email_templates/template1.html", context)