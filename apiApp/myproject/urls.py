from django.contrib import admin
from django.urls import path, include
from api.views import getSimulationState


urlpatterns = [
    path('api/simulation/', getSimulationState, name='getSimulationState'),
]

from django.urls import get_resolver
import sys

resolver = get_resolver()
for pattern in resolver.url_patterns:
    print(pattern, file=sys.stderr)