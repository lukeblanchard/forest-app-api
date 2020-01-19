from rest_framework import serializers

from core.models import Project, Stand, Plot, Tree, TreeReference


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for project objects"""

    class Meta:
        model = Project
        fields = ('id', 'name', 'land_owner',
                  'date', 'metric_system', 'stands')
        read_only_fields = ('id',)


class ProjectDetailSerializer(ProjectSerializer):
    """Serializer for project detail objects"""
    stands = serializers.SerializerMethodField()

    def get_stands(self, obj):
        queryset = obj.stands.all()
        return StandDetailSerializer(queryset, many=True, read_only=True).data


class StandSerializer(serializers.ModelSerializer):
    """Serializer for stand objects"""

    class Meta:
        model = Stand
        fields = ('id', 'project_id', 'identification', 'location',
                  'origin_year', 'size', 'plots')
        read_only_fields = ('id',)


class StandDetailSerializer(StandSerializer):
    """Serializer for stand detail objects"""
    plots = serializers.SerializerMethodField()

    def get_plots(self, obj):
        queryset = obj.plots.all()
        return PlotDetailSerializer(queryset, many=True, read_only=True).data


class PlotSerializer(serializers.ModelSerializer):
    """Serializer for plot objects"""

    class Meta:
        model = Plot
        fields = ('id', 'stand', 'number', 'latitude',
                  'longitude', 'slope', 'aspect', 'trees')
        read_only_fields = ('id',)


class PlotDetailSerializer(PlotSerializer):
    """Serializer for plot detail objects"""
    trees = serializers.SerializerMethodField()

    def get_trees(self, obj):
        queryset = obj.trees.all()
        return TreeSerializer(queryset, many=True, read_only=True).data


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
