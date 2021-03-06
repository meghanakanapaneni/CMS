# Generated by Django 2.1.2 on 2018-12-09 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CMS', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='admintoadmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('admin', models.CharField(max_length=300)),
                ('student_name', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
                ('a_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CMS.college_admin')),
                ('s_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.student')),
            ],
        ),
        migrations.RemoveField(
            model_name='querytoadmin',
            name='a_id',
        ),
        migrations.RemoveField(
            model_name='querytoadmin',
            name='s_id',
        ),
        migrations.RenameField(
            model_name='query',
            old_name='query',
            new_name='admin',
        ),
        migrations.DeleteModel(
            name='Querytoadmin',
        ),
    ]
