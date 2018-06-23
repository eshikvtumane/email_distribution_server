from django.conf.urls import url, include

from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'emails', views.EmailViewSet)
router.register(r'groups-emails', views.GroupEmailViewSet)
router.register(r'periodic-tasks', views.PeriodicTaskViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
