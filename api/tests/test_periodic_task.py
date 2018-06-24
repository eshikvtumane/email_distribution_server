import re
import typing

from helpers.testing.base_function_for_testing_api import *


@pytest.fixture
def periodic_tasks(db):
    return mixer.cycle(5).blend('django_celery_beat.PeriodicTask')

@pytest.fixture
def groups_emails(db):
    return mixer.cycle(5).blend('emails.GroupEmail')

class TestPeriodicTasks(BaseTest):
    url_client = '/api/periodic-tasks/'

    data = {
        "name": "string",
        "interval": {
            'every': 10,
            'period': 'minutes'
        },
        "enabled": True,
        "group_emails": 1
    }

    def get_periodic_task_by_id(self, periodic_task_id):
        return self.get(periodic_task_id)

    def test_get_periodic_tasks_list(self, periodic_tasks):
        response = self.get()
        result_get = response.json()
        print(result_get)
        assert len(result_get) == len(periodic_tasks)

    def test_get_periodic_tasks_by_id(self, periodic_tasks):
        email = periodic_tasks[0]
        response = self.get_periodic_task_by_id(email.id)
        result = response.data
        assert result['id'] == email.id

    def test_post_periodic_task(self, periodic_tasks, groups_emails):
        response_post = self.post(self.data)
        result_post = response_post.json()
        assert ('id' in result_post) == True

        response_get = self.get_periodic_task_by_id(result_post['id'])
        result_get = response_get.json()
        assert ('id' in result_get) == True

    def post_periodic_task_with_interval_parameters(self, invalid_parameter, error_message, interval={}):
        data = self.data.copy()
        data['interval'] = interval

        response_post = self.post(data)
        result_post = response_post.json()
        assert ('interval' in result_post) == True
        assert (invalid_parameter in result_post['interval']) == True
        assert (len(result_post['interval'][invalid_parameter]) > 0) == True

        result = re.search(error_message, result_post['interval'][invalid_parameter][0])
        assert isinstance(result, typing.re.Match) == True

    def test_post_periodic_task_with_empty_interval_parameter_every(self, periodic_tasks):
        self.post_periodic_task_with_interval_parameters('every', 'This field is required.', {'period': 'minutes'})

    def test_post_periodic_task_with_empty_interval_parameter_period(self, periodic_tasks):
        self.post_periodic_task_with_interval_parameters('period', 'This field is required.', {'every': 10})

    def test_post_periodic_task_with_invalid_interval_parameter_period(self, periodic_tasks):
        self.post_periodic_task_with_interval_parameters('period', 'is not a valid choice.',
                                                         {'every': 10, 'period': 'not_period'})

    def test_post_periodic_task_with_invalid_group_emails_id(self, periodic_tasks):
        data = self.data.copy()
        data['group_emails'] = 0
        response_post = self.post(self.data)
        result_post = response_post.json()
        assert ('detail' in result_post) == True
        assert (result_post['detail'] == 'Group with current id not exist') == True


    def test_delete_periodic_task(self, periodic_tasks):
        periodic_task = periodic_tasks[0]

        # check is exist email
        response_get = self.get_periodic_task_by_id(periodic_task.id)
        result_get = response_get.json()
        assert ('id' in result_get) == True
        assert (result_get['id'] == periodic_task.id) == True

        # delete email
        response_delete = self.delete(result_get['id'])
        assert response_delete.status_code == 204

        # check doesn't exist email
        response_get = self.get_periodic_task_by_id(periodic_task.id)
        result_get = response_get.json()
        assert ('detail' in result_get) == True
        assert (result_get['detail'] == 'Not found.') == True

