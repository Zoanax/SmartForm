from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

from scheduler.send_email import welcome_email, send_once_email
from smart_emailApp.models import MyJobModel

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

from datetime import datetime, timedelta

def check_for_task():
    pass




def task_send_welcome_email(email, first_name, last_name, task_name):
    try:
        # Schedule the job to run 1 minute from now
        run_time = datetime.now() + timedelta(seconds=1)
        job = scheduler.add_job(welcome_email(email, first_name, last_name), 'date', run_date=run_time, args=[email, first_name, last_name],
                                name=task_name, jobstore='default')
        print("Task Seheduled")

        # Save the job details to the database
        my_job = MyJobModel(name=job.name, job_id=job.id)
        my_job.save()
        print("Task saved")

        return True
    except:
        return False


def task_one_send_email(email, task_name):
    try:
        # Schedule the job to run 1 minute from now
        run_time = datetime.now() + timedelta(seconds=1)
        job = scheduler.add_job(send_once_email(email,), 'date', run_date=run_time, args=[email,],
                                name=task_name, jobstore='default')
        print("Task Seheduled")

        # Save the job details to the database
        my_job = MyJobModel(name=job.name, job_id=job.id)
        my_job.save()
        print("Task saved")

        return True
    except:
        return False



