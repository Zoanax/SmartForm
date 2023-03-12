from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    welcome_email = models.BooleanField(default=False)
    subscribe_to_newsletter = models.BooleanField(default=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.email}'

    def save(self, *args, **kwargs):
        # validate data
        self.full_clean()

        # save to database
        super(User, self).save(*args, **kwargs)


