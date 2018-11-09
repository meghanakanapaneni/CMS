# Generated by Django 2.1.2 on 2018-11-09 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answerqueryadmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('query', models.CharField(max_length=100)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('mark', models.BooleanField(default=False)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='college_admin',
            fields=[
                ('a_id', models.IntegerField(default='1', primary_key=True, serialize=False)),
                ('ad_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=30)),
                ('apswd', models.CharField(max_length=100)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='course',
            fields=[
                ('c_id', models.IntegerField(default='1', primary_key=True, serialize=False)),
                ('sem_id', models.IntegerField()),
                ('course_name', models.CharField(max_length=100)),
                ('c_credit', models.IntegerField()),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='days',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_id', models.IntegerField()),
                ('day', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('event_id', models.IntegerField(default='1', primary_key=True, serialize=False)),
                ('event_name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=30)),
                ('schedule', models.CharField(max_length=30)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='faculty',
            fields=[
                ('f_id', models.IntegerField(default='1', primary_key=True, serialize=False)),
                ('fac_name', models.CharField(max_length=100)),
                ('ph_no', models.CharField(max_length=15)),
                ('f_email', models.EmailField(max_length=30)),
                ('course_off', models.CharField(max_length=100)),
                ('fpswd', models.CharField(max_length=100)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grades', models.CharField(max_length=30)),
                ('points', models.IntegerField()),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.course')),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=300)),
                ('leave_from', models.DateField()),
                ('leave_to', models.DateField()),
                ('no_ofdays', models.IntegerField()),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='logged',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='logged2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='logged3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Notificationsfromadmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_id', models.IntegerField()),
                ('subject', models.CharField(max_length=100)),
                ('query', models.CharField(max_length=300)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
                ('a_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.college_admin')),
            ],
        ),
        migrations.CreateModel(
            name='Notificationsfromfaculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('query', models.CharField(max_length=300)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
                ('f_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('query', models.CharField(max_length=300)),
                ('student_name', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
                ('f_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Querytoadmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('query', models.CharField(max_length=300)),
                ('student_name', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
                ('a_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CMS.college_admin')),
            ],
        ),
        migrations.CreateModel(
            name='role',
            fields=[
                ('role_id', models.IntegerField(default='1', primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('s_id', models.IntegerField(default='1', primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('sroll_no', models.CharField(max_length=12)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=30)),
                ('sem_id', models.IntegerField()),
                ('cur_yos', models.IntegerField()),
                ('reg_year', models.IntegerField()),
                ('spswd', models.CharField(max_length=100)),
                ('courses', models.CharField(max_length=50)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
                ('role_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.role')),
            ],
        ),
        migrations.CreateModel(
            name='timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeslots', models.CharField(max_length=30)),
                ('courses', models.CharField(max_length=30)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
                ('day_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.days')),
            ],
        ),
        migrations.CreateModel(
            name='UploadSlides',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=20)),
                ('readings', models.CharField(max_length=50)),
                ('docfile', models.URLField(max_length=100)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=45, null=True)),
                ('modified_at', models.DateField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=45, null=True)),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.course')),
                ('f_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.faculty')),
            ],
        ),
        migrations.AddField(
            model_name='querytoadmin',
            name='s_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.student'),
        ),
        migrations.AddField(
            model_name='query',
            name='s_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.student'),
        ),
        migrations.AddField(
            model_name='notificationsfromfaculty',
            name='s_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.student'),
        ),
        migrations.AddField(
            model_name='leave',
            name='s_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.student'),
        ),
        migrations.AddField(
            model_name='grade',
            name='s_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.student'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='role_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.role'),
        ),
        migrations.AddField(
            model_name='course',
            name='f_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CMS.faculty'),
        ),
        migrations.AddField(
            model_name='college_admin',
            name='role_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.role'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='c_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.course'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='s_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.student'),
        ),
        migrations.AddField(
            model_name='answerqueryadmin',
            name='a_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CMS.college_admin'),
        ),
        migrations.AddField(
            model_name='answerqueryadmin',
            name='s_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CMS.student'),
        ),
    ]
