from django.urls import path

from smart_emailApp import views

urlpatterns = [
    #path('', views.form_view, name="form"),
    path('', views.home_view, name='master_home'),
   

]
