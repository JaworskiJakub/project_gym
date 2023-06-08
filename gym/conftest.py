import pytest
from django.test import Client
from gym_app.models import Training, User, UserMembership


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def training():
    return Training.objects.create(
        title='Test Training',
        description='Test Description',
        capacity=10,
        start_time='2023-06-01 10:00:00',
        end_time='2023-06-01 12:00:00'
    )


@pytest.fixture
def active_membership(user):
    return UserMembership.objects.create(
        user=user,
        expiration_date='2024-06-01'
    )
