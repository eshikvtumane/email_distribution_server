import json

from django.db import transaction
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework import serializers
from rest_framework.exceptions import APIException

from emails.submodels.email import Email
from emails.submodels.group_email import GroupEmail
from helpers.celery_tasks import CeleryTasks


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
    task = serializers.ModelField(model_field=PeriodicTask()._meta.get_field('task'), read_only=True)

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
        """
        Create periodic task and interval scheduler from parameters.
        Paraneter group_emails write in kwarg attribute an remove from dict.
        :param validated_data:
        :return:
        """
        interval_key = 'interval'
        group_emails_key = 'group_emails'
        task_key = 'task'
        kwargs_key = 'kwargs'

        try:
            with transaction.atomic():
                interval = self._get_value_by_key(validated_data, interval_key, 'Interval parameter empty')
                interval_obj = IntervalSchedule.objects.create(**interval)
                validated_data[interval_key] = interval_obj

                group_emails = self._get_value_by_key(validated_data, group_emails_key, 'Group emails parameter empty')
                validated_data[kwargs_key] = json.dumps({group_emails_key: group_emails})
                self._remove_value_from_dict_by_key(group_emails_key, validated_data)

                validated_data[task_key] = CeleryTasks.EMAIL_SENDER.value
                result = super(PeriodicTaskSerializer, self).create(validated_data)
                return result
        except Exception as e:
            raise APIException(str(e))


    def _get_value_by_key(self, data_dict, key, exception_error):
        value = data_dict.get(key, None)
        if value is None:
            raise APIException(exception_error)
        return value

    def _remove_value_from_dict_by_key(self, key, data_dict):
        data_dict.pop(key, None)

    def to_representation(self, instance):
        """
        Add group_emails parameter from kwargs attribute
        :param instance:
        :return:  dict
        """
        result = super(PeriodicTaskSerializer, self).to_representation(instance)

        try:
            kwargs = json.loads(result.pop('kwargs', None))
        except:
            raise APIException('Task kwargs parameters contains not in dictionary type.')

        result = {**result, **kwargs}
        return result

