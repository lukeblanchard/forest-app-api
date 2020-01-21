from django.urls import path, include
from rest_framework.routers import DefaultRouter

from forest import views

router = DefaultRouter()
router.register('projects', views.ProjectViewSet)
router.register('projects/(?P<project_id>.+)/stands',
                views.ProjectStandsViewSet,
                basename='project-stand')
router.register('stands', views.StandViewSet)
router.register('stands/(?P<stand_id>.+)/plots',
                views.StandPlotsViewSet,
                basename='stand-plot')
router.register('plots', views.PlotViewSet)
router.register('tree-references', views.TreeReferenceViewSet)
router.register('trees', views.TreeViewSet)
router.register('sample-designs', views.SampleDesignViewSet)

app_name = 'forest'

urlpatterns = [
    path('', include(router.urls))
]
