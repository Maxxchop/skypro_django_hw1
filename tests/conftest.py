from pytest_factoryboy import register

from tests.factories import AdFactory, UserFactory, CategoryFactory

pytest_plugins = "tests.fixtures"


register(AdFactory)
register(UserFactory)
register(CategoryFactory)
