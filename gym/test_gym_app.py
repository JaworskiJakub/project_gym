import pytest
from django.contrib.auth.models import User


def test_index_view(client):
    r = client.get('')
    assert r.status_code == 200


@pytest.mark.django_db
def test_login(client):
    r = client.post('/login/', {'user_name': 'test_user', 'password': 'test_user'})
    assert r.status_code == 200


def test_logout(client):
    r = client.get('/logout/')
    assert r.status_code == 302


@pytest.mark.django_db
def test_create_user(client):
    r = client.post('/add_user/', {
        'user_name': 'pytest_user',
        'password': 'pytest_user',
        'password_rep': 'pytest_user',
        'first_name': 'pytest_name',
        'last_name': 'pytest_surname',
        'email': 'pytest@test.pl'
    })
    assert r.status_code == 302
    assert len(User.objects.filter(username='pytest_user')) == 1


@pytest.mark.django_db
def test_update_profile(client):
    client.post('/login/', {'user_name': 'test_user', 'password': 'test_user'})
    r = client.post('/profile/', {
        'sex': 'kobieta',
        'age': 25,
        'height': 185,
        'weight': 85
    })
    assert r.status_code == 302


@pytest.mark.django_db
def test_profile_info(client):
    client.post('/login/', {'user_name': 'test_user', 'password': 'test_user'})
    r = client.get('/profile_info/')
    assert r.status_code == 302


@pytest.mark.django_db
def test_add_training(client):
    client.post('/login/', {'user_name': 'test_trainer', 'password': 'test_trainer'})
    r = client.post('/add_training/', {
        'title': 'test',
        'description': 'test',
        'trainers': 'test_trainer',
        'capacity': 15,
        'start_time': '2023-06-02T15:00:00',
        'end_time': '2023-06-02T16:00:00'
    })
    assert r.status_code == 302


@pytest.mark.django_db
def test_calendar_view(client):
    r = client.get('/calendar/')
    assert r.status_code == 200


@pytest.mark.django_db
def test_training_view(client):
    r = client.post('/add_training/', {
        'title': 'test',
        'description': 'test',
        'trainers': 'test_trainer',
        'capacity': 15,
        'start_time': '2023-06-02T15:00:00',
        'end_time': '2023-06-02T16:00:00'
    })
    r = client.get('/calendar/training/8/')
    assert r.status_code == 200


@pytest.mark.django_db
def test_memberships(client):
    r = client.get('/purchase/')
    assert r.status_code == 302


@pytest.mark.django_db
def test_add_training(client):
    client.post('/login/', {'user_name': 'test_user', 'password': 'test_user'})
    r = client.get('/add_training/', follow=True)
    assert r.status_code == 200


@pytest.mark.django_db
def test_training_register(client):
    client.post('/login/', {'user_name': 'test_user', 'password': 'test_user'})
    r = client.get('/register_training/50/')
    assert r.status_code == 404


@pytest.mark.django_db
def test_training_info(client):
    client.post('/login/', {'user_name': 'test_user', 'password': 'test_user'})
    r = client.get('/calendar/training/50/')
    assert r.status_code == 500


@pytest.mark.django_db
def test_profile_update(client, profile):
    client.post('/login/', {'user_name': 'tester', 'password': 'tester'})
    r = client.get('/profile_info/')
    assert r.context['age'] == profile.profile.age
    assert r.context['sex'] == profile.profile.sex
    assert r.context['height'] == profile.profile.height
    assert r.context['weight'] == profile.profile.weight

