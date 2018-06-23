from django.conf.urls import url, include
from emails.views import unsubscribe

urlpatterns = [
    url(r'^unsubscribe/(?P<hash>[a-z0-9\-]+)/', unsubscribe, name='unsubscribe'),
]
