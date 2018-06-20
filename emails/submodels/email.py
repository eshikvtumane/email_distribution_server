from django.db import models
from django.db.models import ForeignKey, EmailField


class Email(models.Model):
    email = EmailField()
    group = ForeignKey('emails.GroupEmail')

    def __str__(self):
        return self.email

