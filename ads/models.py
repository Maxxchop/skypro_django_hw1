from django.db import models


class Ad(models.Model):

    name = models.CharField(max_length=100)
    author = models.CharField(max_length=20)
    price = models.IntegerField()
    description = models.TextField(max_length=10000)
    address = models.CharField(max_length=100)
    is_published = models.BooleanField()
