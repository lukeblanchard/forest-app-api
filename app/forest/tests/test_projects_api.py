from django.urls import reverse
from django.test import TestCase

from unittest import mock

from pytz import utc

from datetime import datetime

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project, Stand

from forest.serializers import ProjectSerializer


PROJECTS_URL = reverse('forest:project-list')


def project_stands_url(project_id):
    """Return a project stands URL"""
    return reverse('forest:project-stand-list', args=[project_id])


def detail_url(project_id):
    """Return a project detail URL"""
    return reverse('forest:project-detail', args=[project_id])


def sample_project(**params):
    """Create and return a sample project"""
    defaults = {
        'name': 'Test Project A',
        'land_owner': 'Test Owner A',
        'metric_system': True
    }
    defaults.update(params)

    return Project.objects.create(**defaults)


def sample_stand(project_id, stand_id, **params):
    """Create and return a sample stand"""
    defaults = {
        'project_id': project_id,
        'identification': stand_id,
        'location': 'Test County',
        'origin_year': 1933,
        'size': 20
    }
    defaults.update(params)

    return Stand.objects.create(**defaults)


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

    def test_view_project_detail(self):
        """Test viewing single project detail"""
        project = sample_project()

        url = detail_url(project.id)
        res = self.client.get(url)

        serializer = ProjectSerializer(project)
        self.assertEqual(res.data, serializer.data)

    def test_view_project_stands(self):
        """Test viewing stands for a single project"""
        project = sample_project()
        sample_stand(project, 1)
        sample_stand(project, 2)

        url = project_stands_url(project.id)
        res = self.client.get(url)

        self.assertEqual(len(res.data), 2)
