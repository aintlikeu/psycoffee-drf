import pytest
from rest_framework.test import APIClient

from accounts.models import User
from api.tests.factories import CustomerFactory, SpotFactory


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def admin_client(client):
    admin_user = User.objects.create_superuser(phone="+79998887777", password="password123!")
    client.force_login(admin_user)
    return client


@pytest.fixture
def customer():
    return CustomerFactory.create()


@pytest.fixture
def spot(customer):
    return SpotFactory.create(customer=customer)
