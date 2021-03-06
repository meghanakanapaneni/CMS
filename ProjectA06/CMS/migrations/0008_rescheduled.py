# Generated by Django 2.1.2 on 2018-12-10 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CMS', '0007_auto_20181210_1215'),
    ]

    operations = [
        migrations.CreateModel(
            name='rescheduled',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeslots', models.CharField(max_length=30)),
                ('courses', models.CharField(max_length=30)),
                ('date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
                ('day_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.days')),
            ],
        ),
    ]
