from rest_framework import serializers

from core.models import Project, Stand, Plot, Tree, TreeReference, \
    SampleDesign


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for project objects"""
    class Meta:
        model = Project
        fields = ('id', 'name', 'land_owner',
                  'date', 'measurement_system', 'stands', 'sample_design')
        read_only_fields = ('id', 'stands', 'sample_design',)


class ProjectDetailSerializer(ProjectSerializer):
    """Serializer for project detail objects"""
    stands = serializers.SerializerMethodField()
    sample_design = serializers.SerializerMethodField()

    def get_stands(self, obj):
        queryset = obj.stands.all()
        return StandDetailSerializer(queryset, many=True, read_only=True).data

    def get_sample_design(self, obj):
        queryset = obj.sample_design.all()
        return SampleDesignSerializer(queryset, many=True, read_only=True).data


class SampleDesignSerializer(serializers.ModelSerializer):

    class Meta:
        model = SampleDesign
        fields = ('id', 'sample_type', 'project', 'factor', 'var', 'minv',
                  'maxv')
        read_only_fields = ('id',)


class StandSerializer(serializers.ModelSerializer):
    """Serializer for stand objects"""

    class Meta:
        model = Stand
        fields = ('id', 'project_id', 'identification', 'location',
                  'origin_year', 'size', 'plots')
        read_only_fields = ('id', 'plots')


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
        read_only_fields = ('id', 'trees',)


class PlotDetailSerializer(PlotSerializer):
    """Serializer for plot detail objects"""
    trees = serializers.SerializerMethodField()

    def get_trees(self, obj):
        queryset = obj.trees.all()
        return TreeDetailSerializer(queryset, many=True, read_only=True).data


class TreeReferenceSerializer(serializers.ModelSerializer):
    """Serializer for tree reference objects"""

    class Meta:
        model = TreeReference
        fields = ('id', 'symbol', 'scientific_name',
                  'common_name')
        read_only_fields = ('id',)


class TreeSerializer(serializers.ModelSerializer):
    """Serializer for tree object"""

    class Meta:
        model = Tree
        fields = ('id', 'plot', 'symbol', 'count',
                  'dbh', 'height', 'live_crown_ratio')
        read_only_fields = ('id',)


class TreeRefSymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeReference
        fields = ('symbol')
        read_only_fields = ('symbol',)


class TreeDetailSerializer(TreeSerializer):
    symbol = TreeRefSymbolSerializer(read_only=True)
