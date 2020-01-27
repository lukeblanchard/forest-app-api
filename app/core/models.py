from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Project(models.Model):
    ENG = 'english'
    MET = 'metric'
    SYSTEM_CHOICES[
        (ENG, 'english'),
        (MET, 'metric')
    ]

    name = models.CharField(max_length=255)
    land_owner = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    measurement_system = models.CharField(max_length=8, choices=SYSTEM_CHOICES)

    def __str__(self):
        return self.name


class SampleDesign(models.Model):
    FRQ = 'FRQ'
    BAF = 'BAF'
    SAMPLE_TYPE_CHOICES = [
        (FRQ, 'FRQ'),
        (BAF, 'BAF')
    ]

    HGT = 'HGT'
    DBH = 'DBH'
    VAR_TYPE_CHOICES = [
        (HGT, 'HGT'),
        (DBH, 'DBH')
    ]

    sample_type = models.CharField(max_length=3, choices=SAMPLE_TYPE_CHOICES,
                                   default=None)
    project = models.ForeignKey('Project', on_delete=models.CASCADE,
                                related_name='sample_design')
    factor = models.IntegerField()
    var = models.CharField(max_length=3, choices=VAR_TYPE_CHOICES, default=None)
    minv = models.FloatField()
    maxv = models.FloatField()


class Stand(models.Model):
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE,
                                   related_name='stands')
    identification = models.IntegerField(unique=True)
    location = models.CharField(max_length=255)
    origin_year = models.IntegerField()
    size = models.FloatField()

    def __str__(self):
        return self.location + '::' + str(self.identification)


class Plot(models.Model):
    stand = models.ForeignKey('Stand', on_delete=models.CASCADE,
                              related_name='plots')
    number = models.IntegerField(unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    slope = models.FloatField()
    aspect = models.CharField(max_length=255)

    def __str__(self):
        return str(self.stand) + '::' + str(self.number)


class TreeReference(models.Model):
    symbol = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)
    family = models.CharField(max_length=255)
    max_density_index = models.IntegerField(default=None)

    def __str__(self):
        return self.scientific_name + '::' + self.common_name


class Tree(models.Model):
    plot = models.ForeignKey('Plot', on_delete=models.CASCADE,
                             related_name='trees')
    symbol = models.ForeignKey('TreeReference', on_delete=models.CASCADE)
    count = models.IntegerField()
    dbh = models.FloatField()
    height = models.FloatField()
    live_crown_ratio = models.IntegerField()

    def __str__(self):
        return str(self.plot) + '::' + str(self.symbol)
