# Generated by Django 2.2 on 2020-02-24 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beltexamapp', '0002_auto_20200224_1056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='attendee',
        ),
        migrations.AddField(
            model_name='trip',
            name='attendee',
            field=models.ManyToManyField(related_name='attendees', to='beltexamapp.User'),
        ),
    ]
