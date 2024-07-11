# Generated by Django 5.0.6 on 2024-07-03 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_management', '0005_alter_leave_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='status',
            field=models.IntegerField(choices=[('pending', 0), ('approved', 1), ('rejected', 2), ('pending hr approval', 3)], default='pending'),
        ),
    ]
