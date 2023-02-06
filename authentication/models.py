from django.contrib.auth.models import AbstractUser
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('member', 'Участник')
    ]
    role = models.CharField(max_length=9, choices=ROLE, default='member')
    age = models.IntegerField()
    locations = models.ManyToManyField(Location)
