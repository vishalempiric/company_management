# Generated by Django 5.0.6 on 2024-07-03 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]