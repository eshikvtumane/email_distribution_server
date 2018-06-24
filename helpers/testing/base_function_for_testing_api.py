from urllib import parse

from mixer.backend.django import mixer
from rest_framework.test import APIClient
import pytest

from helpers.testing.locale_fixture import *


@pytest.fixture
def api_client():
    return APIClient()


class BaseTest:
    url_client = None

    def setup_class(self):
        self.api_client = APIClient()

    def url_join(self, *args):
        args = [str(arg) for arg in args]
        url = parse.urljoin(*args) + '/'
        return url

    def get(self, url, format='json'):
        return self.api_client.get(url, format=format)

    def post(self, url, data={}, format='json'):
        return self.api_client.post(url, data, format='json')

    def delete(self, url):
        return self.api_client.delete(url)

