# Generated by Django 2.1.1 on 2019-07-02 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='users_key',
        ),
    ]
