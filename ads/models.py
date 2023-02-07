from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from authentication.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(null=True, unique=True, max_length=10, validators=[MinLengthValidator(5)])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


# class Location(models.Model):
#     name = models.CharField(max_length=100)
#     lat = models.FloatField(null=True)
#     lng = models.FloatField(null=True)
#
#     class Meta:
#         verbose_name = 'Локация'
#         verbose_name_plural = 'Локации'
#
#     def __str__(self):
#         return self.name


# class User(models.Model):
#     ROLE = [
#         ('admin','Администратор'),
#         ('moderator', 'Модератор'),
#         ('member', 'Участник')
#     ]
#     first_name = models.CharField(max_length=20)
#     last_name = models.CharField(max_length=20)
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)
#     role = models.CharField(max_length=9, choices=ROLE, default='member')
#     age = models.IntegerField()
#     locations = models.ManyToManyField(Location)
#
#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'
#
#     def __str__(self):
#         return self.username


class Ad(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(blank=True, max_length=10000)
    is_published = models.BooleanField()
    image = models.ImageField(upload_to='images/', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name
