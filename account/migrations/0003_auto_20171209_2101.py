# Generated by Django 2.0 on 2017-12-09 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('MALE', 'male'), ('FEMALE', 'female')], default='male', max_length=6),
        ),
    ]
