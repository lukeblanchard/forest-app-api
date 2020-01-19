from rest_framework import serializers

from core.models import Project, Stand, Plot, Tree, TreeReference


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for project objects"""

    class Meta:
        model = Project
        fields = ('id', 'name', 'land_owner', 'date', 'metric_system')
        read_only_fields = ('id',)


class StandSerializer(serializers.ModelSerializer):
    """Serializer for stand objects"""
    plots = serializers.SerializerMethodField()

    class Meta:
        model = Stand
        fields = ('id', 'project_id', 'identification', 'location',
                  'origin_year', 'size', 'plots')
        read_only_fields = ('id',)

    def get_plots(self, obj):
        queryset = obj.plots.all()
        return PlotSerializer(queryset, many=True, read_only=True).data

class PlotSerializer(serializers.ModelSerializer):
    """Serializer for plot objects"""

    class Meta:
        model = Plot
        fields = ('id', 'stand', 'number', 'latitude',
                  'longitude', 'slope', 'aspect')
        read_only_fields = ('id',)


class TreeReferenceSerializer(serializers.ModelSerializer):
    """Serializer for tree reference objects"""

    class Meta:
        model = TreeReference
        fields = ('id', 'symbol', 'scientific_name',
                  'common_name', 'family', 'max_density_index')
        read_only_fields = ('id',)


class TreeSerializer(serializers.ModelSerializer):
    """Serializer for tree object"""

    class Meta:
        model = Tree
        fields = ('id', 'plot', 'symbol', 'count',
                  'dbh', 'height', 'live_crown_ratio')
        read_only_fields = ('id',)
