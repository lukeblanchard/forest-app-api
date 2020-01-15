from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Project, Stand, Plot


def sample_user(email='test@testing.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


def sample_project(**params):
    """Create and return a sample project"""
    defaults = {
        'name': 'Test Project A',
        'land_owner': 'Test Owner A',
        'metric_system': True
    }
    defaults.update(params)

    return Project.objects.create(**defaults)


def sample_stand(project, stand_id, **params):
    """Create and return a sample stand"""
    defaults = {
        'project_id': project,
        'identification': stand_id,
        'location': 'Test County',
        'origin_year': 1933,
        'size': 20
    }
    defaults.update(params)

    return Stand.objects.create(**defaults)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating a new user with an email is successful"""
        email = "test@testing.com"
        password = "test1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test the email for a new user is normalized"""
        email = 'test@LONDONAPPDEV.COM'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@testing.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_project_str(self):
        """Test project string representation"""
        project = sample_project()
        self.assertEqual(str(project), project.name)

    def test_stand_str(self):
        """Test stand string representation"""
        project = sample_project()
        stand = sample_stand(project, 3)
        str_rep = stand.location + '::' + str(stand.identification)
        self.assertEqual(str(stand), str_rep)

    def test_plot_str(self):
        """Test plot string representation"""
        project = sample_project()
        stand = sample_stand(project, 4)
        plot = Plot.objects.create(
            stand=stand,
            number=5,
            latitude=36.81808,
            longitude=-81.61263,
            slope=11.123,
            aspect='east'
        )
        str_rep = str(plot.stand) + '::' + str(plot.number)
        self.assertEqual(str(plot), str_rep)
