from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

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


trainer_group, created = Group.objects.get_or_create(name='Trainer')

trainer_group.permissions.add(29)
trainer_group.permissions.add(36)

User.objects.get(username='test_trainer').groups.add(trainer_group)


class Training(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    trainers = models.ManyToManyField(User, limit_choices_to={'groups__name': 'Trainer'})
    capacity = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    registered_users = models.ManyToManyField(User, related_name='registered_trainings', blank=True)

    def __str__(self):
        return self.title


class Membership(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class UserMembership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, null=True)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def is_membership_expired(self):
        if self.expiration_date:
            return self.expiration_date < timezone.now().date()
        return True


class MembershipHistory(models.Model):
    user_membership = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_membership.user.username} - {self.membership.name} - {self.purchase_date}"
