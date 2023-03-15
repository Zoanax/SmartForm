from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

from scheduler.scheduler import Print
from scheduler.send_email import welcome_email, send_once_email
from smart_emailApp.models import MyJobModel



from datetime import datetime, timedelta

def check_for_task():
    pass
import traceback

def task_send_welcome_email(email, first_name, last_name, task_name):
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    try:
        # Schedule the job to run 1 second from now
        run_time = datetime.now() + timedelta(seconds=1)
        print("Adding job to scheduler")
        job = scheduler.add_job(
            welcome_email,
            'date',
            run_date=run_time,
            args=[email, first_name, last_name],
            name=task_name,
            jobstore='default'
        )
        if job:
            update_model(job)
            register_events(scheduler)
            scheduler.start()
            print("Task scheduled: ", job)
            return job
        else:
            print("Job creation failed")
            return False

    except Exception as e:
        print("Error occurred: ", traceback.format_exc())
        return False


def task_one_send_email(email, task_name):
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    try:
        # Schedule the job to run 1 second from now
        run_time = datetime.now() + timedelta(seconds=1)
        print("Adding job to scheduler")
        job = scheduler.add_job(
            send_once_email,
            'date',
            run_date=run_time,
            args=[email],
            name=task_name,
            jobstore='default'
        )
        if job:
            update_model(job)
            register_events(scheduler)
            scheduler.start()
            print("Task scheduled: ", job)
            return job
        else:
            print("Job creation failed")
            return False

    except Exception as e:
        print("Error occurred: ", traceback.format_exc())
        return False


def update_model(job):
    # Save the job details to the database
    my_job = MyJobModel(name=job.name, job_id=job.id)
    my_job.save()
    print("Task saved")


