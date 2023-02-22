from django.urls import path
from .views import *

urlpatterns = [
    path('', Test.as_view())
]
