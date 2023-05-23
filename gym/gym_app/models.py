from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

sexes = (
    (1, 'mężczyzna'),
    (2, 'kobieta'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.IntegerField(choices=sexes, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Training(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    trainers = models.ManyToManyField(User)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


trainer_group, created = Group.objects.get_or_create(name='Trainer')

trainer_group.permissions.add(29)

User.objects.get(username='test_trainer').groups.add(trainer_group)


