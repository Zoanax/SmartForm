import calendar

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

from scheduler.scheduler import Print
from scheduler.send_email import welcome_email, send_once_email, buildEmail
from smart_emailApp.models import MyJobModel, EmailTask
# from smart_emailApp.apps import scheduler

import traceback
from datetime import datetime, timedelta, time


def update_model(job):
    # Save the job details to the database
    my_job = MyJobModel(name=job.name, job_id=job.id)
    my_job.save()
    print("Task saved")

def task_send_welcome_email(email, first_name, last_name, task_name):
    from apscheduler.schedulers.background import BackgroundScheduler
    from django_apscheduler.jobstores import register_events, DjangoJobStore

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    try:
        # Schedule the job to run 1 second from now
        run_time = datetime.now() + timedelta(seconds=30)
        print("Adding job to scheduler ######## ############ ############### ############ ############ #### ")

        job = scheduler.add_job(
            welcome_email,
            'date',
            run_date=run_time,
            args=[email, first_name, last_name],
            name=task_name,
        )
        if job:
            update_model(job)
            register_events(scheduler)
            scheduler.start()
            print("Task scheduled: ", job.id)
            return job
        else:
            print("Job creation failed")
            return False

    except Exception as e:
        print("Error occurred: ", traceback.format_exc())
        return False


def task_one_send_email(email, task_name):
    from apscheduler.schedulers.background import BackgroundScheduler
    from django_apscheduler.jobstores import DjangoJobStore, register_events

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
            #jobstore='default'
        )
        if job:
            update_model(job)
            register_events(scheduler)
            scheduler.start()
            print("Task scheduled: ", job.name)
            return job
        else:
            print("Job creation failed")
            return False

    except Exception as e:
        print("Error occurred: ", traceback.format_exc())
        return False






def task_send_built_email(email_task_id, email_id, task_name, occurence, run_from, run_to):
    from apscheduler.schedulers.background import BackgroundScheduler
    from django_apscheduler.jobstores import register_events, DjangoJobStore

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    trigger = None
    run_time = None
    kwargs = {}

    try:
        # Schedule the job to run based on the provided parameters
        if  occurence == "once":
            run_time = datetime.strptime(run_from, '%Y-%m-%d %H:%M:%S')
            trigger = DateTrigger(run_time, **kwargs)


        elif occurence == "Daily":
            run_time = run_from.time()
            trigger = CronTrigger(hour=run_time.hour, minute=run_time.minute, **kwargs)
            kwargs = {'hour': run_time.hour}

        elif occurence == "Weekly":
            run_time = run_from.time()
            run_date = run_from.date()
            date_str = f"{run_date} {run_time}"
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            day_of_week = date_obj.strftime('%A')
            if day_of_week == 'Sunday':
                day_of_week = 0
            elif day_of_week == 'Monday':
                day_of_week = 1
            elif day_of_week == 'Tuesday':
                day_of_week = 2
            elif day_of_week == 'Wednesday':
                day_of_week = 3
            elif day_of_week == 'Thursday':
                day_of_week = 4
            elif day_of_week == 'Friday':
                day_of_week = 5
            elif day_of_week == 'Saturday':
                day_of_week = 6
            else:
                raise ValueError(f'Invalid weekday name "{day_of_week}"')
            trigger = CronTrigger(hour=run_time.hour, minute=run_time.minute, day_of_week=day_of_week, **kwargs)

            kwargs = {'hour': run_time.hour, 'day_of_week': run_to}



        elif occurence == "Monthly":

            run_time = run_from.time()
            run_day = int(run_to.day)
            run_date = run_from.date().replace(day=run_day)
            date_str = f"{run_date} {run_time}"
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            trigger = CronTrigger(hour=run_time.hour, minute=run_time.minute, day=run_day, **kwargs)


        print("###  SCHEDULE TEST ###")
        job= scheduler.add_job(buildEmail, trigger,  run_date=run_time, args=[email_task_id, email_id], name='test_build-Month', jobstore='default')
        print( '-----------',trigger, run_to,run_from)

        update_model(job)
        register_events(scheduler)
        scheduler.start()

    except Exception as e:
        print("Error occurred: ", traceback.format_exc())
        return False


def check_for_task():
    print('OK')

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
                print("Error in 'check_for_task'function ")
                pass

        if emailtask.date_to_sending <= now:
            print("Expired")
            emailtasks.update(status="Expired")
            print("Changed to Expired")
            return emailtask.id
        else:
            print("Nothing to run###")



