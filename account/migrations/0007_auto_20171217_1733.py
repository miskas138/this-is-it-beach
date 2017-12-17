# Generated by Django 2.0 on 2017-12-17 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20171217_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('SIMPLE_USER', 'simple_user'), ('ADVANCED_USER', 'advanced_user')], default='SIMPLE_USER', max_length=15),
        ),
        migrations.AlterField(
            model_name='advanced_profile',
            name='user_type',
            field=models.CharField(choices=[('SIMPLE_USER', 'simple_user'), ('ADVANCED_USER', 'advanced_user')], default='ADVANCED_USER', max_length=15),
        ),
    ]
