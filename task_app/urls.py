from django.urls import path, include
from .views import *
urlpatterns = [
    path('', schedulerView, name='scheduler'),
    path('check/<int:id>/<slug:week>', checkTask, name='check_task'),
]