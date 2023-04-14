from django.apps import AppConfig


class SmartEmailappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "smart_emailApp"

    def ready(self):
        from apscheduler.schedulers.background import BackgroundScheduler
        from django_apscheduler.jobstores import DjangoJobStore, register_events
        from scheduler.tasks_scheduler import check_for_task
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(check_for_task, 'interval', seconds=200, name="Check_for_tasks")
        register_events(scheduler)
        scheduler.start()


        #tart()
        #update_model(job)


