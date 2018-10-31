from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class role(models.Model):
	role_id = models.AutoField(primary_key=True,default='1')
	role_name = models.CharField(max_length=50)

class student(models.Model):
    s_id = models.AutoField(primary_key=True,default='1')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sroll_no = models.CharField(max_length=12)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    mobile = models.IntegerField()
    email = models.EmailField(max_length=30)
    sem_id = models.IntegerField()
    cur_yos = models.IntegerField()
    reg_year = models.IntegerField()
    role_id = models.ForeignKey(role,on_delete=models.CASCADE)
    created_at = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=45, blank=True, null=True)
    modified_at = models.DateField(blank=True, null=True)
    modified_by = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return str(self.first_name)

	
class faculty(models.Model):
	f_id = models.AutoField(primary_key=True,default='1')
	fac_name = models.CharField(max_length=100)
	froll_no = models.CharField(max_length=30,null=True)
	ph_no = models.CharField(max_length=100)
	course_off = models.CharField(max_length=100)
	role_id = models.ForeignKey(role,on_delete=models.CASCADE)
	created_at = models.DateField(blank=True, null=True)
	created_by = models.CharField(max_length=45, blank=True, null=True)
	modified_at = models.DateField(blank=True, null=True)
	modified_by = models.CharField(max_length=45, blank=True, null=True)


class adm(models.Model):
	a_id = models.AutoField(primary_key=True,default='1')
	ad_name = models.CharField(max_length=100)
	aroll_no = models.CharField(max_length=30)
	role_id = models.ForeignKey(role,on_delete=models.CASCADE)
	apswd = models.CharField(max_length=50)
	created_at = models.DateField(blank=True, null=True)
	created_by = models.CharField(max_length=45, blank=True, null=True)
	modified_at = models.DateField(blank=True, null=True)
	modified_by = models.CharField(max_length=45, blank=True, null=True)

class course(models.Model):
    c_id = models.AutoField(primary_key=True,default='1')
    s_id = models.IntegerField()
    course_name = models.CharField(max_length=100)
    f_id = models.ForeignKey(faculty,on_delete=models.CASCADE,null=True)
    created_at = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=45, blank=True, null=True)
    modified_at = models.DateField(blank=True, null=True)
    modified_by = models.CharField(max_length=45, blank=True, null=True)

class timetable(models.Model):
	day_id = models.IntegerField()
	timeslots = models.CharField(max_length=30)
	c_id = models.ForeignKey(course,on_delete=models.CASCADE)
	created_at = models.DateField(blank=True, null=True)
	created_by = models.CharField(max_length=45, blank=True, null=True)
	modified_at = models.DateField(blank=True, null=True)
	modified_by = models.CharField(max_length=45, blank=True, null=True)

class Grade(models.Model):
	s_id = models.ForeignKey(student,on_delete=models.CASCADE)
	c_id = models.ForeignKey(course,on_delete=models.CASCADE)
	grades = models.CharField(max_length=30)
	created_at = models.DateField(blank=True, null=True)
	created_by = models.CharField(max_length=45, blank=True, null=True)
	modified_at = models.DateField(blank=True, null=True)
	modified_by = models.CharField(max_length=45, blank=True, null=True)

class Attendance(models.Model):
	date = models.DateField()
	s_id = models.ForeignKey(student,on_delete=models.CASCADE)
	c_id = models.ForeignKey(course,on_delete=models.CASCADE)
	mark = models.BooleanField(default=False)
	created_at = models.DateField(blank=True, null=True)
	created_by = models.CharField(max_length=45, blank=True, null=True)
	modified_at = models.DateField(blank=True, null=True)
	modified_by = models.CharField(max_length=45, blank=True, null=True)

class Leave(models.Model):
	s_id = models.ForeignKey(student,on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	leave_roll_no = models.CharField(max_length=100)
	reason = models.CharField(max_length=100)
	leave_from = models.DateField()
	leave_to = models.DateField()
	no_ofdays = models.IntegerField()
	email = models.EmailField(max_length=70,null=True,blank=True)
	created_at = models.DateField(blank=True, null=True)
	created_by = models.CharField(max_length=45, blank=True, null=True)
	modified_at = models.DateField(blank=True, null=True)
	modified_by = models.CharField(max_length=45, blank=True, null=True)

class Query(models.Model):
	query = models.CharField(max_length=100)
	s_id = models.ForeignKey(student,on_delete=models.CASCADE)
	a_id = models.ForeignKey(adm,on_delete=models.CASCADE,null=True)
	created_at = models.DateField(blank=True, null=True)
	created_by = models.CharField(max_length=45, blank=True, null=True)
	modified_at = models.DateField(blank=True, null=True)
	modified_by = models.CharField(max_length=45, blank=True, null=True)
	def __str__(self):
		return self.query

class Answerqueryadmin(models.Model):
	query = models.CharField(max_length=100)
	s_id = models.ForeignKey(student,on_delete=models.CASCADE)
	a_id = models.ForeignKey(adm,on_delete=models.CASCADE,null=True)
	created_at = models.DateField(blank=True, null=True)
	created_by = models.CharField(max_length=45, blank=True, null=True)
	modified_at = models.DateField(blank=True, null=True)
	modified_by = models.CharField(max_length=45, blank=True, null=True)

class Events(models.Model):
	event_id = models.AutoField(primary_key=True,default='1')
	event_name = models.CharField(max_length=30)
	description = models.CharField(max_length=30)
	schedule = models.CharField(max_length=30)
	created_at = models.DateField(blank=True, null=True)
	created_by = models.CharField(max_length=45, blank=True, null=True)
	modified_at = models.DateField(blank=True, null=True)
	modified_by = models.CharField(max_length=45, blank=True, null=True)

