# Generated by Django 2.0 on 2018-02-18 13:42

from django.db import migrations, models
import taggit.managers
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0011_event_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='content',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='section',
            field=models.CharField(choices=[('ΜΟΥΣΙΚΗ', 'Μουσική'), ('ΘΕΑΤΡΟ', 'Θέατρο'), ('ΧΟΡΟΣ', 'Χορός'), ('ΕΚΘΕΣΗ', 'Έκθεση'), ('ΚΙΝΗΜΑΤΟΓΡΑΦΟΣ', 'Κινηματογράφος'), ('ΔΙΑΦΟΡΕΣ', 'Διάφορες')], default='ΜΟΥΣΙΚΗ', max_length=20),
        ),
        migrations.AlterField(
            model_name='event',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='βάλε κομμα αναμεσα στα tag', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
