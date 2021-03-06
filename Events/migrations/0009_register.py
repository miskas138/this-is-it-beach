# Generated by Django 2.0 on 2018-02-13 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Events', '0008_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='register', to='Events.Event')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='register', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
