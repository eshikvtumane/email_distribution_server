from helpers.testing.base_function_for_testing_api import *


@pytest.fixture
def url_client():
    return '/api/groups-emails/'


@pytest.fixture
def groups_emails(db):
    return mixer.cycle(5).blend('emails.GroupEmail')

class TestGroupsEmails(BaseTest):
    url_client = '/api/groups-emails/'

    def get_group_by_id(self, email_id):
        return self.get(self.url_join(self.url_client, email_id))

    def test_get_group_emails_list(self, groups_emails):
        response = self.api_client.get(self.url_client, format='json')
        result_get = response.json()
        assert len(result_get) == len(groups_emails)

    def test_get_group_emails_by_id(self, groups_emails):
        email = groups_emails[0]
        response = self.get_group_by_id(email.id)
        result = response.data
        assert result['id'] == email.id

    def test_post_group_emails(self, groups_emails):
        data = {
            'name': 'GroupTest'
        }

        response_post = self.post(self.url_client, data)
        result_post = response_post.data
        assert ('id' in result_post) == True

        response_get = self.get(self.url_join(self.url_client, result_post['id']))
        result_get = response_get.data
        assert result_get['id'] == result_post['id']

    def test_delete_group_emails(self, groups_emails):
        email = groups_emails[0]

        # check is exist email
        response_get = self.get_group_by_id(email.id)
        result_get = response_get.json()
        assert ('id' in result_get) == True
        assert (result_get['id'] == email.id) == True

        # delete email
        response_delete = self.delete(self.url_join(self.url_client, result_get['id']))
        assert response_delete.status_code == 204

        # check dosn't exist email
        response_get = self.get_group_by_id(email.id)
        result_get = response_get.json()
        assert ('detail' in result_get) == True
        assert (result_get['detail'] == 'Not found.') == True