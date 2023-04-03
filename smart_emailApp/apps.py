from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig



class SmartEmailappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "smart_emailApp"

    def ready(self):
        from scheduler.tasks_scheduler import check_for_task, update_model
        scheduler = BackgroundScheduler()

        scheduler.add_job(check_for_task, 'interval', seconds=60, name="Check_for_tasks")
        scheduler.start()
        #update_model(job)


