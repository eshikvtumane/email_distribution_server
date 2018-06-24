from django.utils.translation import activate
from pytest import fixture


@fixture(autouse=True)
def set_default_language():
    activate('en')
