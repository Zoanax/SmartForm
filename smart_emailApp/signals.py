# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django_apscheduler.models import DjangoJobExecution, DjangoJob
#
# from smart_emailApp.models import Custom_ScheduledJob
# from apscheduler.job import Job as APSchedulerJob
#
#
# print(" SIGNALS>PY file")
#
# @receiver(post_save, sender=DjangoJob)
# def update_scheduled_job(sender, instance, created, **kwargs):
#     print('#######      Signal called! ####################')
#     if created:
#         scheduled_job = Custom_ScheduledJob.objects.create(
#             job_id=instance.id
#         )
#     else:
#         scheduled_job = Custom_ScheduledJob.objects.get(job_id=instance.id)
#     scheduled_job.save()
