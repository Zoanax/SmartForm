from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from SmartForm import settings
from smart_emailApp.models import Emails, EmailTask
from smart_formApp.forms import UserForm
from smart_formApp.models import User


def send_once_email( email):
    # send a confirmation mail
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]

    subject, from_email, to = 'NewsLetter Subscription', email_from, email

    context = {'first_name':"ELG-Fireamrs Member",
               'last_name':"",
               'body': 'Just testing water maybe this will work but it may not work'}

    message_html = render_to_string('email_templates/thankyou.html', context)


    email_message = EmailMessage(subject, '', from_email, recipient_list)
    email_message.content_subtype = "html"
    email_message.body = message_html
    email_message.send()


    print("Email was Sent!!")
    return True


def welcome_email(email, first_name, last_name):
    try:
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

        print("Email was Sent!!################################")
        return True
    except:
        return False




def buildEmail(email_task_id,email_id):
    print("Built Email is running")
    email_task = EmailTask.objects.get(id=email_task_id)
    email_s = Emails.objects.get(id=email_id)

    email_from = settings.EMAIL_HOST_USER

    import ast
    # convert email_task.recipients to a list, because the outputed data from the database is a string of emails.
    email_list = ast.literal_eval(email_task.recipients)

    recipient_list = email_list
    print(recipient_list)

    subject, from_email, to = email_s.subject, email_from, recipient_list

    context ={}
    template_name =""
    product1_image = email_s.product1_image
    product2_image = email_s.product2_image
    product3_image = email_s.product3_image
    product4_image = email_s.product4_image

    if email_s.emailtype=="Store News":
        context = {'receiver': "ELG-Fireamrs Member",
                   'body': email_s.body}
        template_name = "storenews.html"


    elif email_s.emailtype=="Promotional":

        context = {'receiver': "ELG-Fireamrs Member",
                   'body': email_s.body,
                   'product1_image':product1_image,
                   'product2_image':product2_image,
                   'product3_image':product3_image,
                   'product4_image':product4_image,
                   }
        template_name = "storenews.html"

    elif email_s.emailtype=="Seasonal Sales":

        context = {'receiver': "ELG-Fireamrs Member",
                   'body': email_s.body,
                   'product1_image': product1_image,
                   'product2_image': product2_image,
                   'product3_image': product3_image,
                   'product4_image': product4_image,
                   }

        template_name = "storenews.html"

    else:
        pass


    message_html = render_to_string(f'email_templates/'+template_name, context)

    email_message = EmailMessage(subject, '', from_email, recipient_list)
    email_message.content_subtype = "html"
    email_message.body = message_html
    email_message.send()

    print("Built email was sent Email was Sent!!")
    return True