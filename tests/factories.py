import factory.django

from ads.models import Ad, Category
from authentication.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "test"
    password = "123qwe"
    age = 18


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "test"


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    is_published = False
    name = 'test ad name'
    price = 1
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)


