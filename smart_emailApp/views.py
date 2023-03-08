from datetime import datetime, timedelta

from django.shortcuts import render

from smart_formApp.models import User


# Create your views here.

def home_view(request):
    members_count = User.objects.count()
    today = datetime.today()
    thirty_days_ago = today - timedelta(days=7)
    last7days = User.objects.filter(created_at__gte=thirty_days_ago).count()


    context ={
        "members_count": members_count,
        "last7days":last7days

    }

    return render(request, "smartemail/master_home.html", context)
