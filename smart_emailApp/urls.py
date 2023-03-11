from django.urls import path
from smart_emailApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='master_home'),
    path('scheduled_email', views.scheduled_email, name='scheduled_email'),
    path('create_email', views.create_email, name='create_email'),
    path('create_task', views.create_task, name='create_task'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
