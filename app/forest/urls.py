from django.urls import path, include
from rest_framework.routers import DefaultRouter

from forest import views

router = DefaultRouter()
router.register('projects', views.ProjectViewSet)

app_name = 'forest'

urlpatterns = [
    path('', include(router.urls))
]
