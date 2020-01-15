from rest_framework import viewsets

from core.models import Project, Stand

from forest import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    """Manage projects in the database"""
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        """Return objects ordered by name"""
        return self.queryset.order_by('-name')


class ProjectStandsViewSet(viewsets.ModelViewSet):
    """Manage stands associated with a given project_id"""
    queryset = Stand.objects.all()
    serializer_class = serializers.StandSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return self.queryset.filter(project_id=project_id)
