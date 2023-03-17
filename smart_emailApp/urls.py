from django.urls import path
from smart_emailApp import views
from django.conf.urls.static import static
from SmartForm import settings


urlpatterns = [
                  path('', views.home_view, name='master_home'),
                  #path('scheduled_email', views.scheduled_email, name='scheduled_email'),

                  path('view_members', views.member_view, name='view_members'),
                  path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
                  path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

                  path('view_emails', views.email_view, name='view_emails'),
                  path('create_email', views.create_email, name='create_email'),
                  path('delete_email/<int:id>', views.delete_email, name='delete_email'),
                  path('edit_email/<int:id>', views.edit_email, name='edit_email'),
                  path('search_email', views.email_search, name='search_email'),
                  path('view_template/<int:id>', views.email_template_view, name='view_template'),


                  path('edit_task/<int:id>', views.edit_task, name='edit_task'),
                  path('search_task', views.task_search, name='search_task'),
                  path('view_tasks', views.task_view, name='view_tasks'),
                  path('stop_task/<int:id>', views.stop_task, name='stop_task'),
                  path('create_task', views.create_task, name='create_task'),
                  path('view_task_detail/<int:id>', views.task_detail, name='view_task_detail'),
                  path('delete_task/<int:id>', views.delete_task, name='delete_task'),

              ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
