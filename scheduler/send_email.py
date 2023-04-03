from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import  EmailMessage

from django.template.loader import render_to_string

from SmartForm import settings



def send_email(email, first_name, last_name):

    # send a confirmation mail
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]

    subject, from_email, to = 'NewsLetter Subscription', email_from, email

    context = {'first_name':first_name,
               'last_name':last_name,
               'body': 'Just testing water maybe this will work but it may not work'}

    message_html = render_to_string('email_templates/thankyou.html', context)


    email_message = EmailMessage(subject, '', from_email, recipient_list)
    email_message.content_subtype = "html"
    email_message.body = message_html
    email_message.send()


    print("Email was Sent!!")
    return True
