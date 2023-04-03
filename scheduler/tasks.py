from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from smart_emailApp import send_email
from smart_emailApp.models import EmailTask



scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.start()

def schedule_email_task(task_id):
    email_task = EmailTask.objects.get(pk=task_id)
    subject = email_task.emailToSend.subject
    message = email_task.emailToSend.message
    from_email = email_task.sender
    recipient_list = email_task.recipients.split(",")
    scheduler.add_job(send_email, trigger=email_task.task_occurence.lower(), args=[subject, message, from_email, recipient_list], start_date=email_task.date_from, end_date=email_task.date_to_sending, id=str(email_task.pk))

