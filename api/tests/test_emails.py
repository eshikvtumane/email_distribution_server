import re
import typing.re
from urllib import parse

from mixer.backend.django import mixer
from rest_framework.test import APIClient
import pytest

from helpers.testing.locale_fixture import *



@pytest.fixture
def url_client():
    return '/api/emails/'


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def emails(db):
    return mixer.cycle(5).blend('emails.Email')


@pytest.fixture
def email(db):
    return mixer.blend('emails.Email')


def get_email_by_id(api_client, url, email_id):
    url = parse.urljoin(url, '%s/' % email_id)
    return api_client.get(url)


def test_get_emails_list(api_client, emails, url_client):
    response = api_client.get(url_client, format='json')
    result = response.json()
    assert len(result) == len(emails)


def test_get_email_by_id(api_client, emails, url_client):
    email = emails[0]
    response = get_email_by_id(api_client, url_client, email.id)
    result = response.data
    assert result['id'] == email.id


def post_email(api_client, emails, url_client, data):
    response = api_client.post(url_client, data, format='json')
    return response


def test_post_email_with_valid_group(api_client, emails, url_client):
    data = {
        "email": "test@test.ru",
        "subscription": True,
        "group": 1
    }

    response_post = post_email(api_client, emails, url_client, data)
    result_post = response_post.json()

    response_get = get_email_by_id(api_client, url_client, result_post['id'])
    result_get = response_get.json()
    assert ('id' in result_get) == True


def test_post_email_with_invalid_group(api_client, emails, url_client):
    data = {
        "email": "test@test.ru",
        "subscription": True,
        "group": 0
    }

    response_post = post_email(api_client, emails, url_client, data)
    result_post = response_post.json()
    assert ('group' in result_post) == True
    assert (len(result_post['group']) > 0) == True

    pattern = re.compile('Invalid pk "\d+" - object does not exist.')
    pattern_match = pattern.match(result_post['group'][0])
    assert isinstance(pattern_match, typing.re.Match) == True


def test_delete_email(api_client, emails, url_client):
    delete_id = emails[0].id

    # check is exist email
    response_get = get_email_by_id(api_client, url_client, delete_id)
    result_get = response_get.json()
    assert ('id' in result_get) == True
    assert (result_get['id'] == delete_id) == True

    # delete email
    url = parse.urljoin(url_client, '%s/' % delete_id)
    response_delete = api_client.delete(url)
    assert response_delete.status_code == 204

    # check dosn't exist email
    response_get = get_email_by_id(api_client, url_client, delete_id)
    result_get = response_get.json()
    assert ('detail' in result_get) == True
    assert (result_get['detail'] == 'Not found.') == True


def test_create_exist_email(api_client, emails, url_client):
    email = emails[0].email

    data = {
        "email": email,
        "subscription": True,
        "group": 1
    }

    response_post = post_email(api_client, emails, url_client, data)
    result_post = response_post.json()

    assert ('email' in result_post) == True
    assert (len(result_post) != 0) == True
    assert (result_post['email'][0] == 'email with this email already exists.') == True
