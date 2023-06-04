import pytest
from django.test import Client
from gym_app.models import Training, Membership, User, Profile


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def trainers():
    trainer = User.objects.create(
        username='trainer',
        password='trainer',
        password_rep='trainer',
        first_name='trainer',
        last_name='trainer',
        email='trainer@test.com',
    )
    trainer.groups.add(name='Trainer')
    return trainer


@pytest.fixture
def membership():
    m = Membership.objects.create(
        name='Daily',
        duration=1,
        price=10.00
    )
    return m


@pytest.fixture
def profile():
    u = User.objects.create(
        username='tester',
        password='tester',
        first_name='tester',
        last_name='tester',
        email='tester@test.com',
    )
    u.profile.sex = '1'
    u.profile.height = 165
    u.profile.weight = 60
    u.profile.age = 20
    u.save()
    return u
