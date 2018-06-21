import json

from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework import serializers
from rest_framework.exceptions import APIException

from emails.submodels.email import Email
from emails.submodels.group_email import GroupEmail


class GroupEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupEmail
        fields = '__all__'


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'


class IntervalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'


class PeriodicTaskSerializer(serializers.ModelSerializer):
    interval = IntervalScheduleSerializer()
    group_emails = serializers.IntegerField(required=False, write_only=True)
    kwargs = serializers.ModelField(model_field=PeriodicTask()._meta.get_field('kwargs'), read_only=True)

    class Meta:
        model = PeriodicTask
        fields = [
            'name',
            'task',
            'interval',
            'enabled',
            'kwargs',
            'last_run_at',
            'group_emails',
        ]

    def create(self, validated_data):
        interval = validated_data.get('interval', None)
        if interval is not None:
            interval_obj = IntervalSchedule.objects.create(**interval)
            validated_data['interval'] = interval_obj
        else:
            raise APIException('Interval parameter empty')

        group_emails = validated_data.pop('group_emails', None)
        if group_emails is not None:
            validated_data['kwargs'] = json.dumps({'group_emails': group_emails})
        else:
            raise APIException('Group emeils parameter empty')

        return super(PeriodicTaskSerializer, self).create(validated_data)

    def get_group_emails(self):
        pass
