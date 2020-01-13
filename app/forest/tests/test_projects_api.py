from django.urls import reverse
from django.test import TestCase

from unittest import mock

from pytz import utc

from datetime import datetime

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project

from forest.serializers import ProjectSerializer


PROJECTS_URL = reverse('forest:project-list')


class PublicProjectsApiTests(TestCase):
    """Test publicly available project API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_projects(self):
        mock_time = datetime(2020, 1, 13, 0, 0, 0, tzinfo=utc)
        with mock.patch('django.utils.timezone.now',
                        mock.Mock(return_value=mock_time)):
            Project.objects.create(name='Test Project A',
                                   land_owner='Test Owner A',
                                   metric_system=False)
            Project.objects.create(name='Test Project B',
                                   land_owner='Test Owner B',
                                   metric_system=True)

        res = self.client.get(PROJECTS_URL)

        projects = Project.objects.all().order_by('-name')
        serializer = ProjectSerializer(projects, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_project_successful(self):
        """Test creating a new project"""
        payload = {'name': 'Test project C',
                   'land_owner': 'Test Owner C', 'metric_system': True}
        self.client.post(PROJECTS_URL, payload)

        exists = Project.objects.filter(
            name=payload['name'],
            land_owner=payload['land_owner']
        ).exists()
        self.assertTrue(exists)

    def test_create_project_invalid(self):
        """Test creating a project with invalid payload"""
        payload = {'name': '',
                   'land_owner': 'Test Owner C', 'metric_system': True}
        res = self.client.post(PROJECTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
