from django.urls import reverse
from django.test import TestCase

from unittest import mock

from pytz import utc

from itertools import count

from datetime import datetime

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project, Stand, Plot, Tree, TreeReference

from forest.serializers import ProjectSerializer, StandSerializer, \
    ProjectDetailSerializer


PROJECTS_URL = reverse('forest:project-list')
STAND_URL = reverse('forest:stand-list')
PLOT_URL = reverse('forest:plot-list')
TREE_REFERENCE_URL = reverse('forest:treereference-list')
TREE_URL = reverse('forest:tree-list')


def stand_identification(c=count()): return next(c)


def plot_number(c=count()): return next(c)


def project_stands_url(project_id):
    """Return a project stands URL"""
    return reverse('forest:project-stand-list', args=[project_id])


def project_detail_url(project_id):
    """Return a project detail URL"""
    return reverse('forest:project-detail', args=[project_id])


def stand_detail_url(stand_id):
    """Return a project detail URL"""
    return reverse('forest:stand-detail', args=[stand_id])


def stand_plots_url(stand_id):
    """Return a stand plots url"""
    return reverse('forest:stand-plot-list', args=[stand_id])


def sample_project(**params):
    """Create and return a sample project"""
    defaults = {
        'name': 'Test Project A',
        'land_owner': 'Test Owner A',
        'metric_system': True
    }
    defaults.update(params)

    return Project.objects.create(**defaults)


def sample_stand(project_id, **params):
    """Create and return a sample stand"""
    defaults = {
        'project_id': project_id,
        'identification': stand_identification(),
        'location': 'Test County',
        'origin_year': 1933,
        'size': 20
    }
    defaults.update(params)

    return Stand.objects.create(**defaults)


def sample_plot(stand, **params):
    """Create and return a sample plot"""
    defaults = {
        'stand': stand,
        'number': plot_number(),
        'latitude': 41.8781,
        'longitude': -87.6298,
        'slope': 2.5,
        'aspect': 'north'
    }
    defaults.update(params)

    return Plot.objects.create(**defaults)


def sample_tree_reference(**params):
    """Create and return a sample tree reference"""
    defaults = {
        'symbol': 'test symbol',
        'scientific_name': 'test scientific name',
        'common_name': 'test common name',
        'family': 'test family',
        'max_density_index': 200
    }
    defaults.update(params)

    return TreeReference.objects.create(**defaults)


class PublicProjectsApiTest(TestCase):
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

        url = project_detail_url(project.id)
        res = self.client.get(url)

        serializer = ProjectSerializer(project)
        self.assertEqual(res.data, serializer.data)

    def test_view_project_stands(self):
        """Test viewing stands for a single project"""
        project = sample_project()
        project2 = sample_project()
        sample_stand(project)
        sample_stand(project)
        sample_stand(project2)

        url = project_stands_url(project.id)
        res = self.client.get(url)

        self.assertEqual(len(res.data), 2)


class PublicStandsApiTest(TestCase):
    """Test publicly available stands API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_stand_successful(self):
        """Test creating a new stand"""
        project = sample_project()
        payload = {
            'project_id': project.id,
            'identification': 3,
            'location': 'Test County',
            'origin_year': 1933,
            'size': 20
        }
        res = self.client.post(STAND_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        stand = Stand.objects.get(id=res.data['id'])
        for key in payload.keys():
            if key == 'project_id':
                self.assertEqual(project, getattr(stand, key))
            else:
                self.assertEqual(payload[key], getattr(stand, key))

    def test_view_stand_detail(self):
        """Test viewing single stand detail"""
        project = sample_project()
        stand = sample_stand(project)
        url = stand_detail_url(stand.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        stand_data = StandSerializer(stand).data
        project_data = ProjectDetailSerializer(
            stand.project_id).data
        stand_data['sample_design'] = project_data['sample_design']
        stand_data['metric_system'] = project_data['metric_system']

        self.assertEqual(res.data, stand_data)

    def test_view_stand_plots(self):
        """Test viewing plots for a single stand"""
        project = sample_project()
        stand = sample_stand(project)
        sample_plot(stand)
        sample_plot(stand)
        sample_plot(stand)

        url = stand_plots_url(stand.id)
        res = self.client.get(url)
        self.assertEqual(len(res.data), 3)


class PublicPlotsApiTest(TestCase):
    """Test publicly available plots api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_plot_successful(self):
        """Test creating a new plot"""
        project = sample_project()
        stand = sample_stand(project)
        payload = {
            'stand': stand.id,
            'number': 4,
            'latitude': 41.8781,
            'longitude': -87.6298,
            'slope': 2.5,
            'aspect': 'north'
        }

        res = self.client.post(PLOT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        plot = Plot.objects.get(id=res.data['id'])
        for key in payload.keys():
            if key == 'stand':
                self.assertEqual(stand, getattr(plot, key))
            else:
                self.assertEqual(payload[key], getattr(plot, key))


class PublicTreeReferenceApiTest(TestCase):
    """Test publicly available tree reference api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_tree_reference_successful(self):
        """Test creating a new tree reference"""
        payload = {
            'symbol': 't symbol',
            'scientific_name': 'test sn',
            'common_name': 'test cn',
            'family': 'test fam',
            'max_density_index': 295
        }

        res = self.client.post(TREE_REFERENCE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        ref = TreeReference.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(ref, key))


class PublicTreeApiTest(TestCase):
    """Test publicly available tree api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_tree_successful(self):
        """Test creating a new tree"""
        project = sample_project()
        stand = sample_stand(project)
        plot = sample_plot(stand)
        tree_reference = sample_tree_reference()
        payload = {
            'plot': plot.id,
            'symbol': tree_reference.id,
            'count': 10,
            'dbh': 20,
            'height': 70,
            'live_crown_ratio': 40
        }

        res = self.client.post(TREE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        tree = Tree.objects.get(id=res.data['id'])
        for key in payload.keys():
            if key == 'plot':
                self.assertEqual(plot, getattr(tree, key))
            elif key == 'symbol':
                self.assertEqual(tree_reference, getattr(tree, key))
            else:
                self.assertEqual(payload[key], getattr(tree, key))
