from datetime import datetime, timedelta, timezone

from django.shortcuts import render, redirect, get_object_or_404

from SmartForm import settings
from scheduler.send_email import buildEmail
from smart_emailApp.forms import *
from smart_formApp.forms import UserForm
from smart_formApp.models import User


# Create your views here.

def home_view(request):
    from django.db.models import Q

    # buildEmail(1, 1)

    members_count = User.objects.count()
    today = datetime.today()
    thirty_days_ago = today - timedelta(days=7)
    last7days = User.objects.filter(created_at__gte=thirty_days_ago).count()
    numberOf_scheduled_tasks = EmailTask.objects.filter(status="Scheduled").count()
    numberNOt_scheduled_tasks = EmailTask.objects.filter(
        Q(status='Not Scheduled') | Q(status='Expired') | Q(status='STOPPED')).count()
    # only_scheduled_tasks = EmailTask.objects.filter(status="Scheduled")
    only_scheduled_tasks = EmailTask.objects.filter(
        Q(status='Scheduled'),
        updated_at__gte=datetime.now() - timedelta(days=7)
    ).order_by('-date_from')[:3]

    # all_other_task = EmailTask.objects.filter(status="Not Scheduled")

    # not_scheduled_tasks = EmailTask.objects.filter(Q(status='Not Scheduled') | Q(status='Expired')| Q(status='STOPPED'))
    not_scheduled_tasks = EmailTask.objects.filter(
        Q(status='Not Scheduled') | Q(status='Expired') | Q(status='STOPPED'),
        updated_at__gte=datetime.now() - timedelta(days=7)
    ).order_by('-date_to_sending')[:3]

    context = {
        "members_count": members_count,
        "last7days": last7days,
        "numberOf_scheduled_tasks": numberOf_scheduled_tasks,
        "numberNOt_scheduled_tasks": numberNOt_scheduled_tasks,
        'only_scheduled_tasks': only_scheduled_tasks,
        'not_scheduled_tasks': not_scheduled_tasks
    }

    return render(request, "smartemail/master_home.html", context)


def member_view(request):
    limit = 100
    users = User.objects.all()[:limit]
    return render(request, 'smartemail/member_view.html', {'users': users})



def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.email_agreements = request.POST.get('email_agreements') == 'on'
        user.subscribe_to_newsletter = request.POST.get('subscribe_to_newsletter') == 'on'
        user.save()

        return redirect('view_members')

    context = {
        'user': user
    }
    return render(request, 'smartemail/edit_user.html', context)


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('view_members')


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
            form = CreateEmailForm()
    list_info = [
        'Email subject will be used as your email subject and heading when sent!',
        'Please note that the fields related to your products are only used when sending promotional emails or seasonal sales emails. They should not be used for store news emails, as the attachments and product links will not be included in the emails that are sent.',
        'You may still send promotional and sales emails without adding any product information, as those fields are optional.',
        'If you decide to provide product links, make sure that the links work',
    ]

    context = {
        'form': form,
        'what_to_create': "Create Email",
        'submit_btn': 'Create',
        'list_info': list_info,

    }
    return render(request, 'smartemail/create.html', context)


def create_task(request):
    if request.method == 'POST':
        form = EmailTaskForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.status = 'Not Scheduled'
            instance.sender = settings.EMAIL_HOST_USER
            # if user left empty send email to all
            if not instance.recipients:
                members_list = []
                all_memebers = User.objects.filter(subscribe_to_newsletter=True)
                for member in all_memebers:
                    members_list.append(member.email)
                instance.recipients = members_list

            instance.save()

            return redirect('master_home')

            # Process the email task here
    else:
        form = EmailTaskForm()

    list_info = [
        'Task name  fields are required please do not attempt to create tasks without a name',
        'Please leave the recipient fields blank if you want to send an email to all registered members. Alternatively, you can specify the email addresses of the recipients by separating each address with a comma.',
        'Please ensure that you have selected the correct email to send, and also ensure that the scheduled time and frequency are appropriate and make sense.',
        'Note that you can edit and stopped these scheduled tasks at anytime',
    ]

    context = {
        'form': form,
        'list_info': list_info,
        'what_to_create': "Create Email Task",
        'submit_btn': 'Create'
    }
    return render(request, 'smartemail/create.html', context)


def edit_task(request, id):
    task = EmailTask.objects.get(id=id)
    form = EmailTaskForm(request.POST or None, instance=task)
    if form.is_valid():
        intance = form.save(commit=False)
        intance.status = 'Not Scheduled'
        intance.sender = settings.EMAIL_HOST_USER

        # if user left empty send email to all
        if not intance.recipients:
            members_list = []
            all_memebers = User.objects.filter(subscribe_to_newsletter=True)
            for member in all_memebers:
                members_list.append(member.email)
            intance.recipients = members_list

        intance.save()
        return redirect('master_home')
        # Process the email task here

    list_info = [
        'Task name  fields are required please do not attempt to create tasks without a name',
        'Please leave the recipient fields blank if you want to send an email to all registered members. Alternatively, you can specify the email addresses of the recipients by separating each address with a comma.',
        'Please ensure that you have selected the correct email to send, and also ensure that the scheduled time and frequency are appropriate and make sense.',
        'Note that you can edit and stopped these scheduled tasks at anytime',
    ]

    context = {
        'form': form,
        'list_info': list_info,
        'what_to_create': "Create Email Task",
        'submit_btn': 'Update'
    }
    return render(request, 'smartemail/create.html', context)


def stop_task(request, id):
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
        "last7days": last7days,
        "numberOf_scheduled_tasks": numberOf_scheduled_tasks,
        'only_scheduled_tasks': only_scheduled_tasks,
        'not_scheduled_tasks': not_scheduled_tasks
    }
    EmailTask.objects.filter(id=id).update(status="STOPPED")
    return render(request, 'smartemail/master_home.html', context)


def email_view(request):
    emails = Emails.objects.all()
    context = {
        "emails": emails,

    }
    return render(request, "smartemail/emails.html", context)


def email_template_view(request, id):
    emails = Emails.objects.get(id=id)
    print(emails)
    context = {}
    template_name = None
    if emails.emailtype == "Store News":
        context = {'receiver': "ELG-Fireamrs Member",
                   'emails': emails}
        template_name = "storesnews.html"

    elif emails.emailtype == "Promotional":

        context = {'receiver': "ELG-Fireamrs Member",
                   "emails": emails
                   }
        template_name = "onsales.html"

    elif emails.emailtype == "Seasonal Sales":
        context = {
            'receiver': "ELG-Fireamrs Member",
            'emails': emails,
        }
        template_name = "season_specials.html"

    else:
        pass

    return render(request, f"email_templates/" + template_name, context)


def email_search(request):
    search_term = request.GET.get('search-email') or ''
    emails = Emails.objects.filter(subject__contains=search_term)
    print(emails)
    context = {'emails': emails}
    return render(request, 'smartemail/emails.html', context)


def edit_email(request, id):
    email = Emails.objects.get(id=id)
    form = CreateEmailForm(request.POST or None, instance=email)
    if form.is_valid():
        intance = form.save(commit=False)
        # intance.sender = settings.EMAIL_HOST_USER

        intance.save()
        return redirect('view_emails')
    list_info = [
        'Email subject will be used as your email subject and heading when sent!',
        'Please note that the fields related to your products are only used when sending promotional emails or seasonal sales emails. They should not be used for store news emails, as the attachments and product links will not be included in the emails that are sent.',
        'You may still send promotional and sales emails without adding any product information, as those fields are optional.',
        'If you decide to provide product links, make sure that the links work',
    ]

    context = {
        'form': form,
        'what_to_create': "Create Email",
        'submit_btn': 'Update',
        'list_info': list_info,

    }

    return render(request, 'smartemail/create.html', context)
    pass


def delete_email(request, id):
    from django.contrib import messages
    email = Emails.objects.get(id=id)
    associated_tasks = EmailTask.objects.filter(emailToSend=email)

    if request.method == 'POST' and request.POST.get('confirm_delete'):
        email.delete()
        associated_tasks.delete()
        messages.success(request, 'Email and associated tasks deleted successfully.')
        return redirect('view_emails')

    context = {
        'object': email.subject + " Email ",
        'associated_tasks': associated_tasks,
        'back': 'view_emails',

    }

    return render(request, 'smartemail/confirm_delete.html', context)


def task_view(request):
    tasks = EmailTask.objects.all()
    context = {
        "tasks": tasks,

    }
    return render(request, "smartemail/tasks.html", context)


def task_search(request):
    search_term = request.GET.get('search-task') or ''
    tasks = EmailTask.objects.filter(task_name__contains=search_term)
    print(tasks)
    context = {'tasks': tasks}
    return render(request, 'smartemail/tasks.html', context)


def task_detail(request, id):
    return None


def delete_task(request, id):
    from django.contrib import messages
    task = EmailTask.objects.get(id=id)

    if request.method == 'POST' and request.POST.get('confirm_delete'):
        task.delete()
        messages.success(request, 'Tasks deleted successfully.')
        return redirect('view_tasks')

    tasks = EmailTask.objects.all()

    context = {
        'tasks': tasks,
        'object': task.task_name + " Task ",
        'back': 'view_tasks',
    }
    return render(request, 'smartemail/confirm_delete.html', context)



