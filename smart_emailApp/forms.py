from smart_emailApp.models import*
from django import forms
from django.forms import ModelForm


class CreateEmailForm(forms.ModelForm):
    class Meta:
        model = Emails
        exclude =('created_at',)
        fields = ['subject', 'body', 'emailtype', 'product1_image', 'product1_name', 'product1_description',
                  'product1_link', 'product2_image', 'product2_name', 'product2_description', 'product2_link',
                  'product3_image', 'product3_name', 'product3_description', 'product3_link', 'product4_image',
                  'product4_name', 'product4_description', 'product4_link']

        labels = {
            'subject': 'Email Subject',
            'body': 'Email Body Text',
            'emailtype': 'Email Type',

            "product1_image":"Add Image",
            "product1_name":"Product name",
            "product1_description":"Product Description",
            "product1_link":"Product Link",

            "product2_image": "Add Image",
            "product2_name": "Product name",
            "product2_description": "Product Description",
            "product2_link": "Product Link",

            "product3_image": "Add Image",
            "product3_name": "Product name",
            "product3_description": "Product Description",
            "product3_link": "Product Link",

            "product4_image": "Add Image",
            "product4_name": "Product name",
            "product4_description": "Product Description",
            "product4_link": "Product Link"
        }

        widgets = {
            'subject': forms.TextInput(
                attrs={'class': "form-control", }),

            'body': forms.Textarea(
                attrs={'class': "form-control", }),

            'emailtype': forms.Select(
                attrs={'class': "form-control", }),

            "product1_image": forms.FileInput(attrs={'class': 'form-control'}),
            "product1_name": forms.TextInput(attrs={'class': 'form-control'}),
            "product1_description": forms.Textarea(attrs={'class': 'form-control'}),
            "product1_link": forms.URLInput(attrs={'class': 'form-control'}),

            "product2_image": forms.FileInput(attrs={'class': 'form-control'}),
            "product2_name": forms.TextInput(attrs={'class': 'form-control'}),
            "product2_description": forms.Textarea(attrs={'class': 'form-control'}),
            "product2_link": forms.URLInput(attrs={'class': 'form-control'}),

            "product3_image": forms.FileInput(attrs={'class': 'form-control'}),
            "product3_name": forms.TextInput(attrs={'class': 'form-control'}),
            "product3_description": forms.Textarea(attrs={'class': 'form-control'}),
            "product3_link": forms.URLInput(attrs={'class': 'form-control'}),

            "product4_image": forms.FileInput(attrs={'class': 'form-control'}),
            "product4_name": forms.TextInput(attrs={'class': 'form-control'}),
            "product4_description": forms.Textarea(attrs={'class': 'form-control'}),
            "product4_link": forms.URLInput(attrs={'class': 'form-control'}),

        }


class EmailTaskForm(forms.ModelForm):

    recipients = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = EmailTask

        labels ={
            'task_name':"Task name",
            'task_description':"Task Description",
            'task_occurence': "Occurrence",
            'emailToSend': "Choose an email to send",
            'date_from':'Schedule From',
            'date_to_sending':'When to stop',
            'priority':'Priority Level',
        }

        fields = ['task_name', 'task_occurence', 'task_description', 'recipients', 'emailToSend',
                  'date_from', 'date_to_sending',  'priority', ]
        widgets = {

            'task_name': forms.TextInput(attrs={'class': 'form-control'}),
            'task_occurence': forms.Select(attrs={'class': 'form-control'}),
            'task_description': forms.Textarea(attrs={'class': 'form-control'}),
            # 'recipients': forms.TextInput(attrs={'class': "form-control",'placeholder':'Enter email or Leave empty to send to all' },required=False),
            'emailToSend': forms.Select(attrs={'class': 'form-control'}),
            'date_from': forms.DateTimeInput(attrs={'type': 'datetime-local','class': "form-control"}),
            'date_to_sending': forms.DateTimeInput(attrs={'type': 'datetime-local','class': "form-control"}),
            'priority': forms.Select(attrs={'class': 'form-control'})

        }