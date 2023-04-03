from django.utils import timezone

# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def Print():
    today = timezone.now()
    print(today,"Timeeeeeeeeeeeeee#############################################################")



def Start():
    from apscheduler.schedulers.background import BackgroundScheduler
    from django_apscheduler.jobstores import DjangoJobStore, register_events

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # run this job every 24 hours
    scheduler.add_job(Print, 'interval', seconds=4, name='print', jobstore='default')
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...")