# Generated by Django 2.0 on 2018-05-13 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0019_auto_20180512_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='artist_site',
            field=models.URLField(blank=True, null=True),
        ),
    ]