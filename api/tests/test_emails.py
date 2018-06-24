import re
import typing.re

from helpers.testing.base_function_for_testing_api import *


@pytest.fixture
def emails(db):
    return mixer.cycle(5).blend('emails.Email')


@pytest.fixture
def email(db):
    return mixer.blend('emails.Email')


class TestEmails(BaseTest):
    url_client = '/api/emails/'

    def get_email_by_id(self, email_id):
        return self.get(email_id)

    def test_get_emails_list(self, emails):
        response = self.get()
        result = response.json()
        assert len(result) == len(emails)

    def test_get_email_by_id(self, emails):
        email = emails[0]
        response = self.get_email_by_id(email.id)
        result = response.data
        assert result['id'] == email.id

    def test_post_email_with_valid_group(self, emails):
        data = {
            "email": "test@test.ru",
            "subscription": True,
            "group": 1
        }

        response_post = self.post(data)
        result_post = response_post.json()

        response_get = self.get_email_by_id(result_post['id'])
        result_get = response_get.json()
        assert ('id' in result_get) == True

    def test_post_email_with_invalid_group(self, emails):
        data = {
            "email": "test@test.ru",
            "subscription": True,
            "group": 0
        }

        response_post = self.post(data)
        result_post = response_post.json()
        assert ('group' in result_post) == True
        assert (len(result_post['group']) > 0) == True

        pattern = re.compile('Invalid pk "\d+" - object does not exist.')
        pattern_match = pattern.match(result_post['group'][0])
        assert isinstance(pattern_match, typing.re.Match) == True

    def test_delete_email(self, emails):
        email = emails[0]

        # check is exist email
        response_get = self.get_email_by_id(email.id)
        result_get = response_get.json()
        assert ('id' in result_get) == True
        assert (result_get['id'] == email.id) == True

        # delete email
        response_delete = self.delete(email.id)
        assert response_delete.status_code == 204

        # check dosn't exist email
        response_get = self.get_email_by_id(email.id)
        result_get = response_get.json()
        assert ('detail' in result_get) == True
        assert (result_get['detail'] == 'Not found.') == True

    def test_create_exist_email(self, emails):
        email = emails[0].email

        data = {
            "email": email,
            "subscription": True,
            "group": 1
        }

        response_post = self.post(data)
        # response_post = post_email(api_client, emails, url_client, data)
        result_post = response_post.json()

        assert ('email' in result_post) == True
        assert (len(result_post) != 0) == True
        assert (result_post['email'][0] == 'email with this email already exists.') == True