from django_celery_beat.models import PeriodicTask
from rest_framework import viewsets

from api.serializers import GroupEmailSerializer, EmailSerializer, PeriodicTaskSerializer
from emails.submodels.email import Email
from emails.submodels.group_email import GroupEmail


class GroupEmailViewSet(viewsets.ModelViewSet):
    queryset = GroupEmail.objects.all()
    serializer_class = GroupEmailSerializer


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


class PeriodicTaskViewSet(viewsets.ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer
