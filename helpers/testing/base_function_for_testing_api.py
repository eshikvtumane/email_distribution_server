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

    def get(self, id=None, format='json'):
        url = self.url_client
        if id is not None:
            url = self.url_join(self.url_client, id)
        return self.api_client.get(url, format=format)

    def post(self, data={}, format='json'):
        return self.api_client.post(self.url_client, data, format=format)

    def delete(self, id):
        url = self.url_join(self.url_client, id)
        return self.api_client.delete(url)

