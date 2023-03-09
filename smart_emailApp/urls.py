from django.urls import path

from smart_emailApp import views

urlpatterns = [
    path('', views.home_view, name='master_home'),
    path('scheduled_email', views.scheduled_email, name='scheduled_email'),


]
