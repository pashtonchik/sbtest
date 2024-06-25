from rest_framework import routers
from django.urls import path

from testapp.api import test_endpoint

router = routers.DefaultRouter()

urlpatterns = [
    path('api/send/requests/', test_endpoint),
] + router.urls