# Generated by Django 2.0 on 2018-03-11 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Events', '0016_auto_20180309_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mp3Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('mp3', models.FileField(blank=True, null=True, upload_to='event_mp3_uploads/%D/%M/%Y')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mp3_uploads', to='Events.Event')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mp3_uploads', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AlterField(
            model_name='videoupload',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='event_video_uploads/%D/%M/%Y'),
        ),
    ]