# Generated by Django 4.2.1 on 2023-05-23 18:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0004_training'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='training',
            name='name',
        ),
        migrations.AddField(
            model_name='training',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='training',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='training',
            name='title',
            field=models.CharField(default='test', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='training',
            name='description',
            field=models.TextField(),
        ),
    ]