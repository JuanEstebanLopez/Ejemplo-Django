from django.urls import path, include
from .views import schedulerView, checkTask, newTask, newCategory

from rest_framework import routers
from .api import TaskViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', schedulerView, name='scheduler'),
    path('check/<int:id>/<slug:week>', checkTask, name='check_task'),
    path('new_task', newTask, name='new_task'),
    path('new_category', newCategory, name='new_category'),
    path('api/', include(router.urls)),
]