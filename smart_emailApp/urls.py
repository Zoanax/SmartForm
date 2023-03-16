from django.urls import path
from smart_emailApp import views
from django.conf.urls.static import static
from SmartForm import settings


urlpatterns = [
                    path('', views.home_view, name='master_home'),
                    #path('scheduled_email', views.scheduled_email, name='scheduled_email'),
                    path('view_emails', views.email_view, name='view_emails'),
                    path('create_email', views.create_email, name='create_email'),
                    path('create_task', views.create_task, name='create_task'),

                    path('search_email', views.email_search, name='search_email'),
                    path('delete_email/<int:id>', views.delete_email, name='delete_email'),
                    path('edit_email/<int:id>', views.email_search, name='editemail'),


                    path('edit_task/<int:id>', views.edit_task, name='edit_task'),
                    path('view_template/<int:id>', views.email_template_view, name='view_template'),
                    path('stop_task/<int:id>', views.stop_task, name='stop_task'),
              ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
