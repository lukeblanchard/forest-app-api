from rest_framework import viewsets

from core.models import Project, Stand, Plot, Tree, TreeReference

from forest import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    """Manage projects in the database"""
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        """Return objects ordered by name"""
        return self.queryset.order_by('-name')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.ProjectDetailSerializer

        return self.serializer_class


class ProjectStandsViewSet(viewsets.ModelViewSet):
    """Manage stands associated with a given project"""
    queryset = Stand.objects.all()
    serializer_class = serializers.StandSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return self.queryset.filter(project_id=project_id)


class StandViewSet(viewsets.ModelViewSet):
    """Manage stands in the database"""
    queryset = Stand.objects.all()
    serializer_class = serializers.StandSerializer

    def get_queryset(self):
        """Return stands ordered by project_id"""
        return self.queryset.order_by('-project_id')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.StandDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Save stand object"""
        project_id = self.request.POST['project_id']
        project = Project.objects.get(pk=project_id)
        serializer.save(project_id=project)


class StandPlotsViewSet(viewsets.ModelViewSet):
    """Manage plots associated with a given stand"""
    queryset = Plot.objects.all()
    serializer_class = serializers.PlotSerializer

    def get_queryset(self):
        stand_id = self.kwargs['stand_id']
        return self.queryset.filter(stand=stand_id)


class PlotViewSet(viewsets.ModelViewSet):
    """Manage plots in the database"""
    queryset = Plot.objects.all()
    serializer_class = serializers.PlotSerializer

    def get_queryset(self):
        """Return plots ordered by stand"""
        return self.queryset.order_by('-stand')

    def perform_create(self, serializer):
        """Save plot object"""
        stand_id = self.request.POST['stand']
        stand = Stand.objects.get(pk=stand_id)
        serializer.save(stand=stand)


class TreeReferenceViewSet(viewsets.ModelViewSet):
    """Manage tree references in the database"""
    queryset = TreeReference.objects.all()
    serializer_class = serializers.TreeReferenceSerializer

    def get_queryset(self):
        """Return tree references ordered by scientific name"""
        return self.queryset.order_by('-scientific_name')


class TreeViewSet(viewsets.ModelViewSet):
    """Manage trees in the database"""
    queryset = Tree.objects.all()
    serializer_class = serializers.TreeSerializer

    def get_queryset(self):
        """Return trees ordered by plot and symbol"""
        return self.queryset.order_by('-plot', '-symbol')
