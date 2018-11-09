from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
#from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *
from django.shortcuts import render,get_list_or_404
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import requests,json
from datetime import date
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password,check_password
import datetime
import urllib.request
import json 
import pytz
from .models import student
# Create your views here.
def dashboard(request):
	print(request.user)
	return render(request,'its/homepage.html')

def About(request):
    return render(request,'its/About.html')

def Aca1(request):
    return render(request,'its/Aca1.html')

def Aca2(request):
    return render(request,'its/Aca2.html')

def Contact(request):
    return render(request,'its/Contact.html')
    
def facultylogin(request):
    return render(request,'its/facultylogin.html')

def adminlogin(request):
    return render(request,'its/adminlogin.html')

def studenthome(request):
	x=logged.objects.all()[0].sid
	s=student.objects.get(s_id=x)
	template = loader.get_template('its/studenthome.html')
	context = {
		'current':s,
	}
	return render(request,'its/studenthome.html')

def studentlogin(request):
    return render(request,'its/studentlogin.html')
def login1(request):
	if request.method=='POST':
		print(request.user)
		try:
			x = student.objects.get(email=request.POST['email'])
		except(KeyError, student.DoesNotExist):
			template = loader.get_template('its/studentlogin.html')
			context = {
					'IDinvalid':"Invalid Username !",
				}
			return HttpResponse(template.render(context,request))
		if check_password(request.POST['password'], x.spswd) == False:
			template = loader.get_template('its/studentlogin.html')
			context = {
					'Passwordinvalid':"Incorrect password!",
				}
			return HttpResponse(template.render(context,request))

		else:
			logged.objects.all().delete()
			u = logged()
			u.sid = x.s_id
			u.save()
			stu=student.objects.get(s_id=u.sid)
			print(stu.first_name)
			u = logged.objects.all()[0].sid
			s=student.objects.get(s_id=u)
			template = loader.get_template('its/studenthome.html')
			context = {
					'current' : s 
				}
			return HttpResponse(template.render(context,request))

def login2(request):
	if request.method=='POST':
		try:
			x = faculty.objects.get(f_email=request.POST['f_email'])
		except(KeyError, faculty.DoesNotExist):
			template = loader.get_template('its/facultylogin.html')
			context = {
					'IDinvalid':"Invalid Username !",
				}
			return HttpResponse(template.render(context,request))
		if request.POST['password'] != x.fpswd:
			template = loader.get_template('its/facultylogin.html')
			context = {
					'Passwordinvalid':"Incorrect password!",
				}
			return HttpResponse(template.render(context,request))

		else:
			logged2.objects.all().delete()
			u2 = logged2()
			u2.fid = x.f_id
			u2.save()
			u2 = logged2.objects.all()[0].fid
			template = loader.get_template('its/facultyhome.html')
			context = {
					'current' : u2 
				}
			return HttpResponse(template.render(context,request))

def login3(request):
	if request.method=='POST':
		try:
			x = college_admin.objects.get(email=request.POST['email'])
		except(KeyError,college_admin.DoesNotExist):
			template = loader.get_template('its/adminlogin.html')
			context = {
					'IDinvalid':"Invalid Username !",
				}
			return HttpResponse(template.render(context,request))
		if request.POST['apswd'] != x.apswd:
			template = loader.get_template('its/adminlogin.html')
			context = {
					'Passwordinvalid':"Incorrect password!",
				}
			return HttpResponse(template.render(context,request))

		else:
			logged3.objects.all().delete()
			u3 = logged3()
			u3.aid = x.a_id
			u3.save()
			u3 = logged3.objects.all()[0].aid
			template = loader.get_template('its/adminhome.html')
			context = {
					'current' : u3 
				}
			return HttpResponse(template.render(context,request))

# def logout(request):
# 	if logged.objects.count() != 0:

# 	return 

def studentprofile(request):
	x=logged.objects.all()[0].sid
	s=student.objects.get(s_id=x)
	template = loader.get_template('its/studentprofile.html')
	context = {
		'current' : s 
	}
	return HttpResponse(template.render(context,request))

def trackattendance(request):
	x=logged.objects.all()[0].sid
	s=student.objects.get(s_id=x)
	template = loader.get_template('its/trackattendance.html')
	context = {
		'current':s,
	}
	return HttpResponse(template.render(context,request))
	
def trackacademicprogress(request):
	x=logged.objects.all()[0].sid
	s=student.objects.get(s_id=x)
	template = loader.get_template('its/trackacademicprogress.html')
	context = {
		'current' : s 
	}
	return HttpResponse(template.render(context,request))

def studentleave(request):
	x=logged.objects.all()[0].sid
	s=student.objects.get(s_id=x)
	
	if request.method=='POST':
		s_id = x
		reason = request.POST.get('reason', False)
		leave_from = request.POST.get('leave_from', False)
		leave_to = request.POST.get('leave_to', False)
		l1=leave_from.split('-')
		l2=leave_to.split('-')
		d1=date(int(l1[0]),int(l1[1]),int(l1[2]))
		d2=date(int(l2[0]),int(l2[1]),int(l2[2]))
		delta=d2-d1
		no_ofdays = delta.days+1
		created_by = s.first_name
		created_at = datetime.datetime.now().date()
		modified_by = s.first_name
		modified_at = datetime.datetime.now().date()
		p = Leave.objects.create(s_id=s,reason=reason,leave_from=leave_from,leave_to=leave_to,no_ofdays=no_ofdays,created_at = created_at,created_by =  created_by,modified_at= modified_at,modified_by =  modified_by)
		p.save()	
	return render(request,'its/studentleave.html')
def leavesubmit(request):
	x=logged.objects.all()[0].sid
	s=student.objects.get(s_id=x)
	template = loader.get_template('its/leavesubmit.html')
	context = {
		'current' : s 
	}
	return HttpResponse(template.render(context,request))
def adminmakequery(request):
	u = logged.objects.all()[0].sid
	w = student.objects.get(s_id=u)
	v = college_admin.objects.all()	
	template = loader.get_template('its/adminmakequery.html')
	context = {
			'current' : v
		}
	if request.method=='POST':
		admin_name = request.POST.get('admin_name',False)
		admin_row = college_admin.objects.get(ad_name = admin_name)
		#print(admin_row)
		subject = request.POST.get('subject', False)
		query = request.POST.get('query', False)
		created_by = w.first_name
		created_at = datetime.datetime.now().date()
		modified_by = w.first_name
		modified_at = datetime.datetime.now().date()
		p1 = admin_row.querytoadmin_set.create(subject=subject,query=query,s_id_id = u, a_id=admin_row.a_id,created_at= created_at,created_by = created_by,modified_at= modified_at,modified_by= modified_by)
		p1.save()
	return HttpResponse(template.render(context,request))

def facultymakequery(request):
	u = logged.objects.all()[0].sid	
	#print(stu_courses)
	v=student.objects.get(s_id=u)	
	cs=v.courses
	stu_courses=cs.split(',')
	#print(v.courses)
	template = loader.get_template('its/facultymakequery.html')
	context = {
			'current' : {'v':v,'links':stu_courses}
		}
	
	if request.method=='POST':
		course1 = request.POST.get('course',False)
		print(course)
		student_name=v.first_name
		course_row = course.objects.get(course_name = course1)
		faculty_row=faculty.objects.get(f_id=course_row.f_id.f_id)
		subject = request.POST.get('subject', False)
		query = request.POST.get('query', False)
		created_by = v.first_name
		created_at = datetime.datetime.now().date()
		modified_by = v.first_name
		modified_at = datetime.datetime.now().date()
		p = faculty_row.query_set.create(subject=subject,query=query,s_id=v,student_name=student_name,created_at= created_at,created_by = created_by,modified_at= modified_at,modified_by= modified_by)
		p.save()
	return HttpResponse(template.render(context,request))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def facultyprofile(request):
	x=logged2.objects.all()[0].fid
	f=faculty.objects.get(f_id=x)
	template = loader.get_template('its/facultyprofile.html')
	context = {
		'current' : f 
	}
	return HttpResponse(template.render(context,request))

def facultyhome(request):
	x=logged2.objects.all()[0].fid
	f=faculty.objects.get(f_id=x)

	template = loader.get_template('its/facultyhome.html')
	context = {
		'current' : f 
	}
	return HttpResponse(template.render(context,request))
def facultylogin(request):
    return render(request,'its/facultylogin.html')

def answerqueries(request):
    return render(request,'its/answerqueries.html')


def postanswers(request):
	x=logged2.objects.all()[0].fid
	f=faculty.objects.get(f_id=x)
	faculty_queries = f.query_set.all()
	template = loader.get_template('its/facultyhome.html')
	context = {
		'current' : {'f':f , 'faculty_queries' : faculty_queries} 
	}
	return HttpResponse(template.render(context,request))
def facultyanswerqueries(request):
	y=logged2.objects.all()[0].fid
	v=faculty.objects.get(f_id=y)
	if request.method=='POST':
		query = request.POST.get('query', False)
		#a = .notificationsfromadmin_set.objects.create(query=query)
		#a.save()	
	return render(request,'its/facultyanswerqueries.html')
def teaching(request):
	x = logged2.objects.all()[0].fid
	f = faculty.objects.get(f_id = x)
	c = f.course_off
	courses_list = c.split(',')
	print(courses_list)
	context = {
		'courses_list':courses_list,
		'current':f
	}
	return render(request,'its/teaching.html',context)
	
def teachingcourse1(request):
	if request.method == 'POST' and request.FILES['myfile']:
		x=logged2.objects.all()[0].fid
		s=faculty.objects.get(f_id=x)
		f_id = s
		myfile = request.FILES['myfile']
		topic  = request.POST.get('topic')
		readings = request.POST.get('readings')
		# course_name = request.POST.get('course')
		c_obj = course.objects.get(course_name = 'IR')
		fs = FileSystemStorage()
		filename = fs.save('slides/'+ myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		UploadSlides.objects.create(c_id = c_obj, f_id = f_id, topic = topic ,readings = readings,docfile = uploaded_file_url)
		obj = UploadSlides.objects.all()
		obj = list(obj.filter(c_id = c_obj))
		print(obj)
		return render(request, "its/teaching.html")
	else:
		c_obj = course.objects.get(course_name = 'IR')
		obj = UploadSlides.objects.all()
		obj = list(obj.filter(c_id = c_obj))
		return render(request,'its/Teaching/IR.html', {
			'obj': obj
		})

def teachingcourse2(request):
	if request.method == 'POST' and request.FILES['myfile']:
		x=logged2.objects.all()[0].fid
		s=faculty.objects.get(f_id=x)
		f_id = s
		myfile = request.FILES['myfile']
		topic  = request.POST.get('topic')
		readings = request.POST.get('readings')
		# course_name = request.POST.get('course')
		c_obj = course.objects.get(course_name = 'PC')
		fs = FileSystemStorage()
		filename = fs.save('slides/'+ myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		UploadSlides.objects.create(c_id = c_obj, f_id = f_id, topic = topic ,readings = readings,docfile = uploaded_file_url)
		obj = UploadSlides.objects.all()
		obj = list(obj.filter(c_id = c_obj))
		print(obj)
		return render(request, "its/teaching.html")
	else:
		c_obj = course.objects.get(course_name = 'PC')
		obj = UploadSlides.objects.all()
		obj = list(obj.filter(c_id = c_obj))
		return render(request,'its/Teaching/PC.html', {
			'obj': obj
		})


def queries(request):
    return render(request,'its/queries.html')

def details(request):
    return render(request,'its/details.html')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def adminprofile(request):
	z=logged3.objects.all()[0].aid
	a=college_admin.objects.get(a_id=z)
	template = loader.get_template('its/adminprofile.html')
	context = {
		'current' : a 
	}
	return HttpResponse(template.render(context,request))

def adminlogin(request):
    return render(request,'its/adminlogin.html')

def adminhome(request):
	z=logged3.objects.all()[0].aid
	a=college_admin.objects.get(a_id=z)
	template = loader.get_template('its/adminhome.html')
	context = {
		'current' : a 
	}
	return HttpResponse(template.render(context,request))

def addevents(request):
	z=logged3.objects.all()[0].aid
	a=college_admin.objects.get(a_id=z)
	template = loader.get_template('its/addevents.html')
	context = {
		'current' : a 
	}
	if request.method=='POST':
		e = Events.objects.count()
		event_name = request.POST.get('event_name', False)
		description = request.POST.get('description', False)
		schedule = request.POST.get('schedule', False)
		p = Events.objects.create(event_id=e+1,event_name=event_name,description=description,schedule=schedule)
		p.save()		
		return HttpResponse("Successfully saved")
	return render(request,'its/addevents.html')

def addfaculty(request):
	z=logged3.objects.all()[0].aid
	a=college_admin.objects.get(a_id=z)
	template = loader.get_template('its/addfaculty.html')
	context = {
		'current' : a 
	}
	if request.method=='POST':
		f = faculty.objects.count()
		fac_name = request.POST.get('fac_name', False)
		froll_no = request.POST.get('froll_no', False)
		ph_no = request.POST.get('ph_no', False)
		course_off = request.POST.get('course_off', False)
		description = request.POST.get('description', False)
		role_id_id = 2
		fpswd = make_password(request.POST.get('fpswd', False))
		created_by = a.ad_name
		created_at = datetime.datetime.now().date()
		modified_by = a.ad_name
		modified_at = datetime.datetime.now().date()

		p = faculty.objects.create(f_id=f+1,fac_name=fac_name,froll_no=froll_no,ph_no=ph_no,course_off=course_off,description=description,role_id_id=role_id_id,fpswd=fpswd)
		p.save()		
		return HttpResponse("Successfully saved")
	return render(request,'its/addfaculty.html')


def addstudent(request):
	z=logged3.objects.all()[0].aid
	a=college_admin.objects.get(a_id=z)
	template = loader.get_template('its/addstudent.html')
	context = {
		'current' : a 
	}
	s = student.objects.all()
	if request.method=='POST':
		email = request.POST.get('email')
		sroll_no = request.POST.get('sroll_no', False)
		if s.filter(email = email) and s.filter(sroll_no = sroll_no):
			return HttpResponse("student already exists") 
		else:
			s = student.objects.count()
			first_name = request.POST.get('first_name', False)
			last_name = request.POST.get('last_name', False)
			
			dob = request.POST.get('dob', False)
			gender = request.POST.get('gender', False)
			mobile = request.POST.get('mobile', False)
			spswd = make_password(request.POST.get('spswd', False))
			courses = request.POST.get('courses',False)
			
			role_id_id = 1
			sem_id = request.POST.get('sem_id', False)
			cur_yos = request.POST.get('cur_yos', False)
			reg_year = request.POST.get('reg_year', False)
			created_by = a.ad_name
			created_at = datetime.datetime.now().date()
			modified_by = a.ad_name
			modified_at = datetime.datetime.now().date()
			p = student.objects.create(s_id=s+1,first_name=first_name,last_name=last_name,sroll_no=sroll_no,dob=dob,gender=gender,mobile=mobile,spswd=spswd,courses= courses,email=email,role_id_id=role_id_id,sem_id=sem_id,cur_yos=cur_yos,reg_year=reg_year,created_at= created_at,created_by = created_by,modified_at= modified_at,modified_by= modified_by)
			p.save()		
	return render(request,'its/addstudent.html')
	
def adminanswerqueries(request):
	
	z=logged3.objects.all()[0].aid
	v=college_admin.objects.get(a_id=z)
	template = loader.get_template('its/adminanswerqueries.html')
	context = {
		'current' : a 
	}	
	return HttpResponse(template.render(context,request))

def adminevents(request):
	z=logged3.objects.all()[0].aid
	v=college_admin.objects.get(a_id=z)
	all_events = Events.objects.all()
	template = loader.get_template('its/adminevents.html')
	context = {
		'current' : {'all_events' : all_events, 'v': v} 
	}	
	return HttpResponse(template.render(context,request))
def adminfaculty(request):
	z=logged3.objects.all()[0].aid
	v=college_admin.objects.get(a_id=z)
	all_faculty = faculty.objects.all()
	template = loader.get_template('its/adminfaculty.html')
	context = {
		'current' : {'all_faculty' : all_faculty, 'v': v} 
	}	
	return HttpResponse(template.render(context,request))	



def adminqueries(request):
	z=logged3.objects.all()[0].aid
	v=college_admin.objects.get(a_id=z)
	all_queries = v.querytoadmin_set.all()
	print('retrieved')
	template = loader.get_template('its/adminqueries.html')
	context = {
			'current' : {'admin_queries' : all_queries, 'v': v} 
		}
	return HttpResponse(template.render(context,request))

def adminstudents(request):
	z=logged3.objects.all()[0].aid
	v=college_admin.objects.get(a_id=z)
	all_students = student.objects.all()
	template = loader.get_template('its/adminstudents.html')
	context = {
		'current' : {'all_students' : all_students, 'v': v} 
		}
	return HttpResponse(template.render(context,request))
def authenticate(token):
	url = "https://serene-wildwood-35121.herokuapp.com/oauth/getDetails"
	Payload = {'token' : token,'secret' : "32b29bfed559049a7cb82c01088b3c07759d820dfb99e43a2ecf9ef31baf31e5645679e9f99966f7911117e149fce474d2591b87da6f9f0464780853b6aea652"} 
	k = requests.post(url,Payload)
	
	details = json.loads(k.content.decode('utf-8'))
	print(details)	
	return details

def callback(request,token):
	info = authenticate(token)
	template = loader.get_template('its/studenthome.html')
	student_data = info['student']
	s_id = student_data[0]['Id']
	sroll_no = student_data[0]['Student_ID']
	student_first_name = student_data[0]['Student_First_Name']
	student_middle_name = student_data[0]['Student_Middle_Name']
	student_last_name = student_data[0]['Student_Last_name']
	student_dob = student_data[0]['Student_DOB']
	student_gender = student_data[0]['Student_Gender']
	student_email = student_data[0]['Student_Email']
	student_mobile = student_data[0]['Student_Mobile']
	student_mother_tongue = student_data[0]['Student_Mother_Tongue']
	# student_registered_year = student_data[0]['Student_Registered_Year']
	student_registered_degree = student_data[0]['Student_Registered_Degree']
	student_registered_degree_duration = student_data[0]['Student_Registered_Degree_Duration']
	student_cur_yearofstudy = student_data[0]['Student_Cur_YearofStudy']
	student_cur_sem = student_data[0]['Student_Cur_Sem']
	student_academic_status = student_data[0]['Student_Academic_Status']
	rand_password = "student@123"
	# try:
	stu_obj = student.objects.get(email = student_email)
	# except student.DoesNotExist:
	# 	stu_obj = None
	# if stu_obj is None:
	# 	student.objects.create(s_id=s_id,first_name=student_first_name,last_name=student_last_name,sroll_no=sroll_no,dob=student_dob,
	# 		gender=student_gender,mobile=student_mobile,spswd=rand_password,
	# 		email=student_email,role_id_id=1,sem_id=student_cur_sem,cur_yos=student_cur_yearofstudy,reg_year=student_registered_year,
	# 		created_at= datetime.datetime.now().replace(tzinfo=pytz.UTC).date(),created_by = student_first_name,modified_at= datetime.datetime.now().replace(tzinfo=pytz.UTC).date(),modified_by= student_first_name)
	# 	student = student.objects.get(s_id = s_id)

	# 	return render(request, 'its/studenthome.html', {
	# 		'current': student
	# 	})
	logged.objects.create(sid = s_id)
	context = {'current':stu_obj}
	if stu_obj.email == student_email:
		print(student)
		return  HttpResponse(template.render(context,request))
	
