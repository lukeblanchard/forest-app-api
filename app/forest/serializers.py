from rest_framework import serializers

from core.models import Project, Stand


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for project objects"""

    class Meta:
        model = Project
        fields = ('id', 'name', 'land_owner', 'date', 'metric_system')
        read_only_fields = ('id',)


class StandSerializer(serializers.ModelSerializer):
    """Serializer for stand objects"""
    project_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stand
        fields = ('id', 'project_id', 'identification', 'location',
                  'origin_year', 'size')
        read_only_fields = ('id', 'project_id',)
