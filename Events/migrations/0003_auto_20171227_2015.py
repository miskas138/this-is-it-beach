# Generated by Django 2.0 on 2017-12-27 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0002_auto_20171227_1952'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='location_name',
            new_name='name',
        ),
    ]