# Generated by Django 2.2.3 on 2019-07-24 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freetry', '0004_auto_20190724_1328'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='second_filed',
            new_name='second_field',
        ),
    ]