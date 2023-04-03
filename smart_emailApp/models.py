from django.db import models


class Emails(models.Model):
    email_type = (
        ('Promotional', 'Promotional'),
        ('Store News', 'Store News'),
        ('Seasonal Sales', 'Seasonal Sales'),
    )

    subject = models.CharField(max_length=100)
    body = models.TextField(max_length=1000)
    emailtype = models.CharField(max_length=50, choices=email_type, null=True)

    # Image attachment, name and Description
    product1_image = models.ImageField(upload_to="email_imageAttachment/", null=True, blank=True, default=None)
    product1_name = models.CharField(max_length=60, null=True, blank=True)
    product1_description = models.CharField(max_length=200, null=True, blank=True)
    product1_link = models.URLField(max_length=100, null=True, blank=True)

    product2_image = models.ImageField(upload_to="email_imageAttachment/", null=True, blank=True, default=None)
    product2_name = models.CharField(max_length=60, null=True, blank=True)
    product2_description = models.CharField(max_length=200, null=True, blank=True)
    product2_link = models.URLField(max_length=100, null=True, blank=True)

    product3_image = models.ImageField(upload_to="email_imageAttachment/", null=True, blank=True, default=None)
    product3_name = models.CharField(max_length=60, null=True, blank=True)
    product3_description = models.CharField(max_length=200, null=True, blank=True)
    product3_link = models.URLField(max_length=100, null=True, blank=True)

    product4_image = models.ImageField(upload_to="email_imageAttachment/", null=True, blank=True, default=None)
    product4_name = models.CharField(max_length=60, null=True, blank=True)
    product4_description = models.CharField(max_length=200, null=True, blank=True)
    product4_link = models.URLField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.emailtype} || {self.subject}'

    def save(self, *args, **kwargs):
        # validate data
        self.full_clean()

        # save to database
        super(Emails, self).save(*args, **kwargs)


class EmailTask(models.Model):
    task_type = (
        ('Once', 'Once'),
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    )

    task_status = (
        ('Scheduled', 'Scheduled'),
        ('STOPPED', 'STOPPED'),
        ('Not Scheduled', 'Not Scheduled'),
        ('Expired', 'Expired'),
    )

    priority_level = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )

    task_name = models.CharField(max_length=200)
    task_occurence = models.CharField(max_length=50, choices=task_type, null=True, blank=True)
    task_description = models.TextField(max_length=200)
    recipients = models.CharField(max_length=1000)

    sender = models.EmailField()
    emailToSend = models.ForeignKey(Emails, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    date_from = models.DateTimeField()
    date_to_sending = models.DateTimeField()

    status = models.CharField(max_length=50, choices=task_status, null=True, blank=True)
    priority = models.CharField(max_length=50, choices=priority_level, null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.task_name} || {self.task_occurence} || {self.status}'


class MyJobModel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    job_id = models.CharField(max_length=255)
    decription = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    # Add any other fields you need to store information about the job

    def __str__(self):
        return self.name


class Link(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'subject', 'url')

    views = models.PositiveIntegerField(default=0)

    def increment_views(self):
        self.views += 1
        self.save()

    def __str__(self):
        return f'Product name: {self.name} || {self.url} || views:  {self.views} '
