from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@testing.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


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
        project = models.Project.objects.create(
            name='Test Project',
            land_owner='Test Owner',
            metric_system=True)
        self.assertEqual(str(project), project.name)

    def test_stand_str(self):
        """Test stand string representation"""
        project = models.Project.objects.create(
            name='Test Project A',
            land_owner='Test Owner A',
            metric_system=True)

        stand = models.Stand.objects.create(
            project_id=project,
            identification=3,
            location='Albemarle County',
            origin_year=1945,
            size=54.5
        )
        str_rep = stand.location + '::' + str(stand.identification)
        self.assertEqual(str(stand), str_rep)
