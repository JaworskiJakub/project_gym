# Generated by Django 4.2.1 on 2023-05-14 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.IntegerField(blank=True, choices=[(1, 'mężczyzna'), (2, 'kobieta')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weight',
            field=models.IntegerField(blank=True),
        ),
    ]
