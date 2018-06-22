from enum import Enum

from django.db import models
from django.db.models import fields


class Status(Enum):
    SUCCESS = 'success'
    FAILURE = 'failure'

    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class EmailSenderLogger(models.Model):
    message = fields.TextField()
    error = fields.TextField()
    status = fields.CharField(max_length=255, choices=Status.choices(), default=Status.SUCCESS.name)
    datetime_end = fields.DateTimeField(auto_now_add=True)
