# Generated by Django 2.0 on 2017-12-27 17:52

from django.db import migrations, models
import django.db.models.deletion
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField()),
                ('ticket_price', models.FloatField()),
                ('presale', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('tel', models.IntegerField()),
                ('city', models.CharField(max_length=20)),
                ('site', models.URLField(blank=True)),
                ('position', geoposition.fields.GeopositionField(max_length=42)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='section',
            field=models.CharField(choices=[('ΜΟΥΣΙΚΗ', 'Μουσική'), ('ΘΕΑΤΡΟ', 'Θέατρο'), ('ΧΟΡΟΣ', 'Χορός'), ('ΕΚΘΕΣΗ', 'Έκθεση'), ('ΚΙΝΗΜΑΤΟΓΡΑΦΟΣ', 'Κινηματογράφος')], default='ΜΟΥΣΙΚΗ', max_length=20),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='location',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Events.Event'),
        ),
        migrations.AddField(
            model_name='information',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Events.Event'),
        ),
    ]