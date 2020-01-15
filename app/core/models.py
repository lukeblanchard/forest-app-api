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
    name = models.CharField(max_length=255)
    land_owner = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    metric_system = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Stand(models.Model):
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE)
    identification = models.IntegerField(unique=True)
    location = models.CharField(max_length=255)
    origin_year = models.IntegerField()
    size = models.FloatField()

    def __str__(self):
        return self.location + '::' + str(self.identification)


class Plot(models.Model):
    stand = models.ForeignKey('Stand', on_delete=models.CASCADE)
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
    max_density_index = models.FloatField()

    def __str__(self):
        return self.scientific_name


class Tree(models.Model):
    plot = models.ForeignKey('Plot', on_delete=models.CASCADE)
    symbol = models.ForeignKey('TreeReference', on_delete=models.CASCADE)
    count = models.IntegerField()
    dbh = models.FloatField()
    height = models.FloatField()
    live_crown_ratio = models.FloatField()

    def __str__(self):
        return str(self.plot) + '::' + str(self.symbol)
