import pytest
from django.test import Client
from gym_app.models import Training, Membership


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def training():
    t = Training.objects.create(
        title='test',
        description='test',
        trainers='test_trainer',
        capacity=15,
        start_time='2023-06-02T15:00:00',
        end_time='2023-06-02T16:00:00'
    )
    return t


@pytest.fixture
def membership():
    m = Membership.objects.create(
        name='Daily',
        duration=1,
        price=10.00
    )
    return m
