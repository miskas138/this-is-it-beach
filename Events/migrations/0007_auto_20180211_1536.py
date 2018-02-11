# Generated by Django 2.0 on 2018-02-11 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0006_location_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='Events.Event'),
        ),
    ]