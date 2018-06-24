from mixer.backend.django import mixer
from rest_framework.test import APIClient
import pytest

from helpers.testing.locale_fixture import *


@pytest.fixture
def api_client():
    return APIClient()
