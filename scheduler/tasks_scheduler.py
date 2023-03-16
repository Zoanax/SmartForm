from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore, register_events
from scheduler.send_email import welcome_email, send_once_email, buildEmail
from smart_emailApp.models import MyJobModel, EmailTask
import traceback
from datetime import datetime, timedelta, time


def update_model(job):
    # Save the job details to the database
    my_job = MyJobModel(name=job.name, job_id=job.id)
    my_job.save()
    print("Task saved")
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


# def task_send_built_email(email_task_id,email_id, task_name, occurence,run_from, run_to):
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#     try:
#         # Schedule the job to run 1 second from now
#         run_time = datetime.now() + timedelta(seconds=1)
#         print("Adding job to scheduler")
#         job = scheduler.add_job(
#             buildEmail,
#             'date',
#             run_date=run_time,
#             args=[email_task_id,email_id],
#             name=task_name,
#             jobstore='default'
#         )
#
#         if job:
#             update_model(job)
#             register_events(scheduler)
#             scheduler.start()
#             print("Task scheduled: ", job)
#             return job
#         else:
#             print("Job creation failed")
#             return False
#
#     except Exception as e:
#         print("Error occurred: ", traceback.format_exc())
#         return False


def task_send_built_email(email_task_id, email_id, task_name, occurence, run_from, run_to):
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    trigger = None
    run_time = None
    kwargs = {}

    try:
        # Schedule the job to run based on the provided parameters
        if occurence == "once":
            run_time = datetime.strptime(run_from, '%Y-%m-%d %H:%M:%S')
            trigger = 'date'
        elif occurence == "daily":
            run_time = datetime.strptime(run_from, '%H:%M:%S')
            trigger = 'cron'
            kwargs = {'hour': run_time.hour, 'minute': run_time.minute}
        elif occurence == "weekly":
            run_time = datetime.strptime(run_from, '%H:%M:%S')
            trigger = 'cron'
            kwargs = {'hour': run_time.hour, 'minute': run_time.minute, 'day_of_week': run_to}

        job = scheduler.add_job(
            buildEmail,
            trigger,
            run_date=run_time,
            args=[email_task_id, email_id],
            name=task_name,
            jobstore='default',
            **kwargs if occurence != "once" else {}
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



def check_for_task():
    from datetime import datetime
    import pytz

    # Get the current time in UTC
    now_utc = datetime.now(pytz.utc)

    # Convert UTC time to Eastern Standard Time (EST)
    eastern = pytz.timezone('US/Eastern')
    now = now_utc.astimezone(eastern)

    # Print the EST time in a specific format
    print(now.strftime('%Y-%m-%d %H:%M:%S %Z'))
    print(now)

    from django.db.models import Q
    emailtasks = EmailTask.objects.filter(Q(status='Not Scheduled') | Q(status='Scheduled'))


    for emailtask in emailtasks:
        if (emailtask.status=="Not Scheduled"):
            print("HERE NOW 1")
            try:
                #email = EmailTask.objects.filter()
                print(emailtask)
                task_name =emailtask.task_name
                occurence = emailtask.task_occurence
                run_from = emailtask.date_from
                run_to = emailtask.date_to_sending
                print(f"###########  Email ID of the email to send  "+str(emailtask.emailToSend))

                task_send_built_email(emailtask.id, emailtask.emailToSend.id, task_name,occurence,run_from,run_to)
                emailtasks.update(status="Scheduled")
                print("Changed to Scheduled")
                return emailtask.id
            except:
                pass

        if emailtask.date_to_sending <= now:
            print("Expired")
            emailtasks.update(status="Expired")
            print("Changed to Expired")
            return emailtask.id
        else:
            print("Nothing to run###")



