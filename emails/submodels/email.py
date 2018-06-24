import random

from django.db import models
from django.db.models import ForeignKey, EmailField


def create_hash():
    return "%032x" % random.getrandbits(128)


class Email(models.Model):

    email = EmailField(unique=True)
    group = ForeignKey('emails.GroupEmail')

    verification_hash = models.CharField(max_length=32, default=create_hash, unique=True)
    subscription = models.BooleanField(default=True)

    def __str__(self):
        return self.email

