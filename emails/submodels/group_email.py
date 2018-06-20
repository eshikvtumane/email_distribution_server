from django.db import models
from django.db.models import CharField


class GroupEmail(models.Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name
