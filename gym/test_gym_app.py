import pytest
from django.contrib.auth.models import User, Group
from gym_app.models import Training
from django.urls import reverse
from django.test import RequestFactory
from gym_app.views import TrainingView


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
        'weight': 850
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
def test_memberships(client):
    r = client.get('/purchase/')
    assert r.status_code == 302


@pytest.mark.django_db
def test_add_training(client):
    client.post('/login/', {'user_name': 'test_user', 'password': 'test_user'})
    r = client.get('/add_training/', follow=True)
    assert r.status_code == 200


@pytest.mark.django_db
def test_training_detail_view(client):
    trainers_group = Group.objects.create(name='Trainer')
    user = User.objects.create_user(username='testuser', password='testpassword')
    training = Training.objects.create(
        title='Test Training',
        description='Test Training Description',
        capacity=10,
        start_time='2023-06-01 10:00:00',
        end_time='2023-06-01 12:00:00',
    )
    training.trainers.add(user)
    trainers_group.user_set.add(user)
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('training_details', args=[training.pk]))
    assert response.status_code == 200
    assert training.title.encode() in response.content
    assert training.description.encode() in response.content


@pytest.mark.django_db
def test_training_detail_view_invalid_id(client):
    trainers_group = Group.objects.create(name='Trainer')
    user = User.objects.create_user(username='testuser', password='testpassword')
    trainers_group.user_set.add(user)
    client.login(username='testuser', password='testpassword')
    factory = RequestFactory()
    invalid_training_id = 9999
    request = factory.get(reverse('training_details', args=[invalid_training_id]))
    try:
        TrainingView.as_view()(request, id=invalid_training_id)
    except Training.DoesNotExist:
        pass
    else:
        raise AssertionError("Expected Http404 not raised.")


@pytest.mark.django_db
def test_redirect_without_active_membership(client, user, training):
    client.login(username='testuser', password='testpassword')
    response = client.post(reverse('training_register', args=[training.pk]))
    assert response.status_code == 302
    assert response.url == reverse('purchase_membership')


@pytest.mark.django_db
def test_redirect_if_already_registered(client, user, training, active_membership):
    client.login(username='testuser', password='testpassword')
    training.registered_users.add(user)
    response = client.post(reverse('training_register', args=[training.pk]))
    assert response.status_code == 200
    assert 'You are already enrolled!' in response.content.decode()
