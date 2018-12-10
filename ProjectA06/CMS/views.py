from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
#from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *
from django.shortcuts import render,get_list_or_404
from django.template import loader
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import requests,json
from datetime import date
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password,check_password
import datetime
import urllib.request
import json 
import pytz
from .models import student
import operator
from django.db.models import Q
import openpyxl
# Create your views here.
def dashboard(request):
	#print(request.user)
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


def studentlogin(request):
    return render(request,'its/studentlogin.html')
@ csrf_protect 
def login1(request):
	if request.method=='POST':
		#print(request.user)
		try:
			x = student.objects.get(email=request.POST['email'])
		except(KeyError, student.DoesNotExist):
			template = loader.get_template('its/studentlogin.html')
			context = {
					'IDinvalid':"Invalid Username !",
				}
			return HttpResponse(template.render(context,request))
		if check_password(request.POST['password'] , x.spswd)==False:
			template = loader.get_template('its/studentlogin.html')
			context = {
					'Passwordinvalid':"Incorrect password!",
				}
			return HttpResponse(template.render(context,request))

		else:
			request.session["id"] = x.s_id
			logged.objects.all().delete()
			u = logged()
			u.sid = x.s_id
			u.save()
			stu=student.objects.get(s_id=u.sid)
			u = logged.objects.all()[0].sid
			s=student.objects.get(s_id=u)
			template = loader.get_template('its/studenthome.html')
			queries_fac = Notificationsfromfaculty.objects.filter(s_id = s.s_id).only('f_id','subject','query')
			queries_from_admin =Notificationsfromadmin.objects.filter(s_id = s.s_id).only('a_id','subject','query')
			template = loader.get_template('its/studenthome.html')
			
			if(queries_fac.count() == 0):
				message="No notifications from faculty"
			else:	
				message = "Notifications"
				
			if(queries_from_admin.count() == 0):
				message1="No notifications from admin"
			else:	
				message1 = "Notifications"
			context = {
				'current':s,
				'queries_from_admin':queries_from_admin,
				'queries':queries_fac,
				'message':message,
				'message1':message1,
			}
			return HttpResponse(template.render(context,request))



def studenthome(request):
	if(request.session.get("id", False) != False):
		x=logged.objects.all()[0].sid
		s=student.objects.get(s_id=x)
		queries_fac = Notificationsfromfaculty.objects.filter(s_id = s.s_id).only('f_id','subject','query')
		queries_from_admin =Notificationsfromadmin.objects.filter(s_id = s.s_id).only('a_id','subject','query')
		template = loader.get_template('its/studenthome.html')
		
		if(queries_fac.count() == 0):
			message="No notifications from faculty"
		else:	
			message = "Notifications"
			
		if(queries_from_admin.count() == 0):
			message1="No notifications from admin"
		else:	
			message1 = "Notifications"
		print(message,message1)
		context = {
				'current':s,
				'queries_from_admin':queries_from_admin,
				'queries':queries_fac,
				'message':message,
				'message1':message1,
			}
		return render(request,'its/studenthome.html',context)
	else:
		return redirect('homepage')

def logout(request):
	request.session.flush()
	return redirect('homepage') 

def studentprofile(request):
	if(request.session.get("id", False) != False):
		x=logged.objects.all()[0].sid
		s=student.objects.get(s_id=x)
		template = loader.get_template('its/studentprofile.html')
		context = {
			'current' : s ,
		}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')



def trackacademicprogress(request):
	if(request.session.get("id",False)!=False):
		x=logged.objects.all()[0].sid
		s=student.objects.get(s_id=x)
		g=Grade.objects.filter(s_id=x)
		sum=0
		credit_sum=0
		for i in g:
			#print(i.points)
			c=course.objects.get(c_id=i.c_id.c_id)
			sum=sum+(i.points*c.c_credit)
			credit_sum=credit_sum+c.c_credit

		cgpa=float("{0:.2f}".format(sum/credit_sum))
		template = loader.get_template('its/trackacademicprogress.html')
		context = {
				'current' : {'sem':range(1,s.sem_id),'s':s ,'cgpa':cgpa}
			}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')


def trackaca1(request):
    if(request.session.get("id",False)!=False):
        u=logged.objects.all()[0]
        # print("-------------")
        #print(u.sem_id)
        x=u.sid
        #print("hello")
        
        if request.method=='POST':
            
            semes = request.POST.get('semes',False)
            
            number = request.POST.get('prev',False)
            print(number)
            logged.objects.all().delete()
            u = logged()
            u.sid = x
            if number == '1':
                u.sem_id=int(semes)-1
            elif number == '2' :
                u.sem_id=int(semes)+1
            else:
                u.sem_id = int(semes)
            u.save()
    
        
        x=logged.objects.all()[0].sid
        #print(semes)
        #print(u.sem_id)
        semes=u.sem_id
        sem_id1=logged.objects.all()[0].sem_id
        s=student.objects.get(s_id=x)
        g=Grade.objects.filter(s_id=x)
        sum1=0
        credit_sum=0
        for i in g:
            c=course.objects.get(c_id=i.c_id.c_id)
            if(c.sem_id==sem_id1):
                    sum1=sum1+(i.points*c.c_credit)
                    credit_sum=credit_sum+c.c_credit
        sgpa=("%.2f" % round((sum1/credit_sum),2))
        #print("***")
        #print(int(semes))
        template = loader.get_template('its/trackaca1.html')
        context = {
            'current' : { 's':s,'g':g ,'sgpa':sgpa , 'sem_id':sem_id1 ,'semes':int(semes)} 
        }
        return HttpResponse(template.render(context,request))
    else:
        return redirect('homepage')


def studentleave(request):
	if(request.session.get("id",False)!=False):
		x=logged.objects.all()[0].sid
		s=student.objects.get(s_id=x)
		alertmessage="Leave successfully applied"
		context = {
			'current':{ 's':s }
		}
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
			context = {
				'current':{ 's':s , 'alertmessage':alertmessage }
			}
			return render(request,'its/studentleave.html',context)
		return render(request,'its/studentleave.html',context)
	else:
		return redirect('homepage')

def leavesubmit(request):
	if(request.session.get("id",False)!=False):
		x=logged.objects.all()[0].sid
		s=student.objects.get(s_id=x)
		template = loader.get_template('its/leavesubmit.html')
		context = {
			'current' : s 
		}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')

def adminmakequery(request):
	if(request.session.get("id",False)!=False):
		u = logged.objects.all()[0].sid
		w = student.objects.get(s_id=u)
		v = college_admin.objects.all()	
		template = loader.get_template('its/adminmakequery.html')
		
		context = {
				'current' : w,
				'admin_obj':v,
			}
		if request.method=='POST':
			admin_name = request.POST.get('admin_name',False)
			admin_row = college_admin.objects.get(ad_name = admin_name)
			subject = request.POST.get('subject', False)
			query = request.POST.get('query', False)
			created_by = w.first_name
			created_at = datetime.datetime.now().date()
			modified_by = w.first_name
			modified_at = datetime.datetime.now().date()
			print((QuerytoAdmin.objects.filter(query=query, s_id_id=u)).count())
			if(((QuerytoAdmin.objects.filter(query=query,s_id_id=u)).count())>0):
				alertmessage="Query already posted"				
			else:
				p1 = admin_row.querytoadmin_set.create(subject=subject,query=query,s_id_id = u,student_name=w.first_name,a_id=admin_row.a_id,created_at= created_at,created_by = created_by,modified_at= modified_at,modified_by= modified_by)
				p1.save()
				alertmessage="Query successfully posted"
			context = {
				'current' : w,
				'admin_obj':v,
				'alertmessage':alertmessage,
			}	
			return HttpResponse(template.render(context,request))
			
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')

def facultymakequery(request):
	if(request.session.get("id",False)!=False):
		u = logged.objects.all()[0].sid		
		s=student.objects.get(s_id=u)
		v=registeredcourses.objects.get(s_id=u)	
		cs=v.courses
		stu_courses=cs.split(',')
		template = loader.get_template('its/facultymakequery.html')
		
		context = {
				'current' : {'links':stu_courses ,'s':s}
			}
		
		if request.method=='POST':
			course1 = request.POST.get('course',False)
			#print(course)
			student_name=s.first_name
			course_row = course.objects.get(course_name = course1)
			faculty_row=faculty.objects.get(f_id=course_row.f_id.f_id)
			subject = request.POST.get('subject', False)
			f_query = request.POST.get('query', False)
			#if Query.objects.filter(f_id = faculty_row.f_id) :
			created_by = s.first_name
			created_at = datetime.datetime.now().date()
			modified_by = s.first_name
			modified_at = datetime.datetime.now().date()
			if(((Query.objects.filter(query=f_query) and Query.objects.filter(s_id_id=u)).count())>0):
				alertmessage="Query already posted"
			else:
				p = faculty_row.query_set.create(subject=subject,query=f_query,s_id=s,student_name=student_name,created_at= created_at,created_by = created_by,modified_at= modified_at,modified_by= modified_by)
				p.save()
				alertmessage="Query successfully posted"
			context = {
				'current' : {'links':stu_courses ,'s':s},
				'alertmessage':alertmessage,
			}
			return render(request,'its/facultymakequery.html',context)				
		return HttpResponse(template.render(context,request))				
	else:
		return redirect('homepage')
def slides(request):
	if(request.session.get("id",False)!=False):
		u = logged.objects.all()[0].sid	
		s=student.objects.get(s_id=u)
		v=registeredcourses.objects.get(s_id=u)	
		cs=v.courses
		stu_courses=cs.split(',')
		
		template = loader.get_template('its/slides.html')

		if request.method == "POST":
			courses = request.POST.get("course")
			#print(courses)
			c_obj = course.objects.get(course_name = courses)
			obj = UploadSlides.objects.all()
			obj = list(obj.filter(c_id = c_obj))
			if(len(obj) == 0):
				message="No slides"
			else:
				message = "Slides"
			return render(request,'its/slides.html', {
				'message':message,
				'course':c_obj,
				'obj': obj,
				'current' : {'links':stu_courses ,'s':s}
			})	
		return HttpResponse(template.render({'current' : {'links':stu_courses ,'s':s}},request))
	else:
		return redirect('homepage')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@csrf_protect 
def login2(request):
	if request.method=='POST':
		try:
			x = faculty.objects.get(f_email=request.POST['f_email'])
		except(KeyError, faculty.DoesNotExist):
			template = loader.get_template('its/facultylogin.html')
			context = {
					'IDinvalid':"Invalid Username !",
				}
			return HttpResponse("Invalid Username")
		
		if check_password(request.POST['password'] ,x.fpswd) ==False:
			template = loader.get_template('its/facultylogin.html')
			context = {
					'Passwordinvalid':"Incorrect password!",
				}
			return HttpResponse("Incorrect password")

		else:
			logged2.objects.all().delete()
			u2 = logged2()
			u2.fid = x.f_id
			u2.save()
			u2 = logged2.objects.all()[0].fid
			request.session["fid"] = x.f_id
			request.session["femail"] = x.f_email
			template = loader.get_template('its/facultyhome.html')
			f=faculty.objects.get(f_id=u2)
			q = Query.objects.filter(f_id = u2)
			template = loader.get_template('its/facultyhome.html')
			if(q.count() == 0):
				message = "No queries to display"
			else:
				message = "queries"
			context = {
				'message':message,
				'current' : f ,
				'queries' : q,
			}
			return HttpResponse(template.render(context,request))
				
def facultyprofile(request):
	if(request.session.get("fid",False)!=False):
		x=logged2.objects.all()[0].fid
		f=faculty.objects.get(f_id=x)
		template = loader.get_template('its/facultyprofile.html')
		context = {
			'current' : f 
		}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')
def facultyhome(request):
	if(request.session.get("fid",False)!=False):
		x=logged2.objects.all()[0].fid
		f=faculty.objects.get(f_id=x)
		q = Query.objects.filter(f_id= x)
		template = loader.get_template('its/facultyhome.html')
		
		if(q.count() == 0):
			message = "No queries to display"
		else:
			message = "queries"
		print(message)	
		context = {
			'message':message,
			'current' : f ,
			'queries' : q,
		}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')

def facultylogin(request):
    return render(request,'its/facultylogin.html')


def postanswers(request):
	if(request.session.get("fid",False)!=False):
		x=logged2.objects.all()[0].fid
		f=faculty.objects.get(f_id=x)
		faculty_queries = Query.objects.filter(f_id = x)
		template = loader.get_template('its/postanswers.html')
		if(faculty_queries.count() == 0):
			message = "No queries to display"
		else:
			message = "queries"

		context = {
			'message':message,
			'current' : {'f':f ,
   		 	'faculty_queries' : faculty_queries
				}, 
		}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')

def facultyanswerqueries(request):
	if(request.session.get("fid",False)!=False):
		y=logged2.objects.all()[0].fid
		if request.method=='POST':
			student_id = request.POST.get('student_id')
			query_id = request.POST.get('query_id')
			query = request.POST.get('query')
		
		v=faculty.objects.get(f_id=y)
		if(student_id==None):
			r = Notificationsfromfaculty.objects.get(f_id_id=y,query="Nothing")
			q1=r.subject
			s1=r.s_id
			created_by = v.fac_name
			created_at = datetime.datetime.now().date()
			modified_by = v.fac_name
			modified_at = datetime.datetime.now().date()
			print(query)
			p = Notificationsfromfaculty.objects.create(subject=q1,query=query,s_id=s1,f_id_id=y,created_at= created_at,created_by = created_by,modified_at= modified_at,modified_by= modified_by)
			p.save()
			Notificationsfromfaculty.objects.filter(query="Nothing").delete()
		else:
			q=Query.objects.get(id=query_id)
			created_by = v.fac_name
			created_at = datetime.datetime.now().date()
			modified_by = v.fac_name
			modified_at = datetime.datetime.now().date()
			p = Notificationsfromfaculty.objects.create(f_id_id=y,query="Nothing",s_id=student_id,subject=q.subject,created_at= created_at,created_by = created_by,modified_at= modified_at,modified_by= modified_by)
			p.save()	
		template = loader.get_template('its/facultyanswerqueries.html')
		alert_message = "Answer posted"
		context = {
			'current' : v ,
			'alert message':alert_message,
		}	
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')

# def teaching(request):
# 	x = logged2.objects.all()[0].fid
# 	f = faculty.objects.get(f_id = x)
# 	c = f.course_off
# 	courses_list = c.split(',')
# 	print(courses_list)
# 	context = {
# 		'courses_list':courses_list,
# 		'current':f
# 	}
# 	return render(request,'its/teaching.html',context)
	
def teaching(request):
	if(request.session.get("fid",False)!=False):
		x = logged2.objects.all()[0].fid
		f = faculty.objects.get(f_id = x)
		c = f.course_off
		courses_list = c.split(',')
		#print(courses_list)
		context = {
			'courses_list':courses_list,
			'current':f
		}
		if request.method == 'POST' and request.FILES['myfile']:
			x=logged2.objects.all()[0].fid
			s=faculty.objects.get(f_id=x)
			course_name = request.POST.get('course')
			#print(course_name)
			c_obj = course.objects.get(course_name = course_name)
			f_id = s
			myfile = request.FILES['myfile']
			topic  = request.POST.get('topic')
			readings = request.POST.get('readings')
			fs = FileSystemStorage()
			filename = fs.save('slides/'+ myfile.name, myfile)
			uploaded_file_url = fs.url(filename)
			if (UploadSlides.objects.filter(topic = topic)) != False:  
				created_by = s.fac_name
				created_at = datetime.datetime.now().date()
				modified_by = s.fac_name
				modified_at = datetime.datetime.now().date()
				UploadSlides.objects.create(c_id = c_obj, f_id = f_id, topic = topic ,readings = readings,docfile = uploaded_file_url,created_at=created_at,created_by=created_by,modified_at=modified_at,modified_by=modified_by)
				obj = UploadSlides.objects.all()
				obj = list(obj.filter(c_id = c_obj))
				#print(obj)
				alertmessage="Slides are successfully posted"
				return render(request, "its/teaching.html",{
					'obj' :obj,
					'courses_list':courses_list,
					'current':f,
					'alertmessage': alertmessage,
				})
		return render(request,'its/teaching.html',context)
	else:
		return redirect('homepage')

	

	
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@csrf_protect 
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
		if check_password(request.POST['apswd'] , x.apswd)==False:
			template = loader.get_template('its/adminlogin.html')
			context = {
					'Passwordinvalid':"Incorrect password!",
				}
			return HttpResponse(template.render(context,request))

		else:
			request.session["aid"] = x.a_id
			logged3.objects.all().delete()
			u3 = logged3()
			u3.aid = x.a_id
			u3.save()
			u3 = logged3.objects.all()[0].aid
			a = college_admin.objects.get(a_id=u3)
			template = loader.get_template('its/adminhome.html')
			queries_to_admin = QuerytoAdmin.objects.filter(a_id = a)
			l = Leave.objects.all()
			context = {
			'current' : a ,
			'leave':l,
			'queries':queries_to_admin,
			}
			
			return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')	
def adminprofile(request):
	if(request.session.get("aid",False)!=False):
		z=logged3.objects.all()[0].aid
		a=college_admin.objects.get(a_id=z)
		template = loader.get_template('its/adminprofile.html')
		context = {
			'current' : a 
		}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')
def adminlogin(request):
	return render(request,'its/adminlogin.html')
def adminhome(request):
	if(request.session.get("aid",False)!=False):
		z=logged3.objects.all()[0].aid
		a=college_admin.objects.get(a_id=z)
		l = Leave.objects.all()
		s = len(student.objects.all())
		q = len(QuerytoAdmin.objects.all())
		e = len(Events.objects.all())
		f = len(faculty.objects.all())
		queries_to_admin = QuerytoAdmin.objects.filter(a_id = z)
		template = loader.get_template('its/adminhome.html')
		context = {
			'current' : a ,
			's':s,
			'q':q,
			'e':e,
			'f':f,
			'leave':l,
			'queries':queries_to_admin,
		}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')
def addevents(request):
	if(request.session.get("aid",False)!=False):
		z=logged3.objects.all()[0].aid
		a=college_admin.objects.get(a_id=z)
		template = loader.get_template('its/addevents.html')
		context = {
				'current' : a,
				}	
		if request.method=='POST':
			e = Events.objects.count()
			event_name = request.POST.get('event_name', False)
			if Events.objects.filter(event_name = event_name) != False:
				description = request.POST.get('description', False)
				schedule = request.POST.get('schedule', False)
				p = Events.objects.create(event_id=e+1,event_name=event_name,description=description,schedule=schedule)
				p.save()
				alertmessage="Event successfully addded"
				context = {
				'current' : a,
				'alertmessage':alertmessage,
				}		
				return render(request,'its/addevents.html',context)
			else:
				alertmessage="Event already addded"
				context = {
				'current' : a,
				'alertmessage':alertmessage,
				}	
				return render(request,'its/addevents.html',context)
		return render(request,'its/addevents.html',context)
	else:
		return redirect('homepage')
def addfaculty(request):
	if(request.session.get("aid",False)!=False):
		z=logged3.objects.all()[0].aid
		a=college_admin.objects.get(a_id=z)
		template = loader.get_template('its/addfaculty.html')
		context = {
				'current' : a, 
		}	
		if request.method=='POST':
			f = faculty.objects.count()
			fac_name = request.POST.get('fac_name', False)
			froll_no = request.POST.get('froll_no', False)
			if faculty.objects.get(fac_name = fac_name) != False:
				ph_no = request.POST.get('ph_no', False)
				course_off = request.POST.get('course_off', False)
				description = request.POST.get('description', False)
				role_id_id = 2
				fpswd = make_password("faculty@123")
				created_by = a.ad_name
				created_at = datetime.datetime.now().date()
				modified_by = a.ad_name
				modified_at = datetime.datetime.now().date()
				p = faculty.objects.create(f_id=f+1,fac_name=fac_name,froll_no=froll_no,ph_no=ph_no,course_off=course_off,description=description,role_id_id=role_id_id,fpswd=fpswd)
				p.save()
				alertmessage="Faculty successfully added"
				context = {
							'current' : a,
							'alertmessage':alertmessage, 
						}		
				return render(request,'its/addfaculty.html',context)
			else:
				alertmessage="Faculty already exists"
				context = {
							'current' : a,
							'alertmessage':alertmessage, 
						}
				return render(request,'its/addfaculty.html',context)
		return render(request,'its/addfaculty.html',context)
	else:
		return redirect('homepage')

def addstudent(request):
	if(request.session.get("aid",False)!=False):
		z=logged3.objects.all()[0].aid
		a=college_admin.objects.get(a_id=z)
		template = loader.get_template('its/addstudent.html')
		s = student.objects.all()
		context = {
			'current' : a,
		}
		if request.method=='POST':
			email = request.POST.get('email')
			sroll_no = request.POST.get('sroll_no', False)
			if s.filter(email = email) and s.filter(sroll_no = sroll_no):
				alertmessage="Student already exists"
				context = {
							'current' : a,
							'alertmessage':alertmessage, 
						}
				return render(request,'its/addstudent.html',context)
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
				alertmessage="Student successfully addded"
				context = {
							'current' : a,
							'alertmessage':alertmessage, 
						}
				return render(request,'its/addstudent.html',context)		
		return render(request,'its/addstudent.html',context)
	else:
		return redirect('homepage')
def adminanswerqueries(request):
	if(request.session.get("aid",False)!=False):
		z=logged3.objects.all()[0].aid
		if request.method=='POST':
			student_id = request.POST.get('student_id')
			query_id = request.POST.get('query_id')
			query = request.POST.get('query')
		
		v=college_admin.objects.get(a_id=z)
		if(student_id==None):
			r = Notificationsfromadmin.objects.get(a_id_id=z,query="Nothing")
			q1=r.subject
			s1=r.s_id
			created_by = v.ad_name
			created_at = datetime.datetime.now().date()
			modified_by = v.ad_name
			modified_at = datetime.datetime.now().date()
			p = Notificationsfromadmin.objects.create(subject=q1,query=query,s_id=s1,a_id_id=z,created_at= created_at,created_by = created_by,modified_at= modified_at,modified_by= modified_by)
			p.save()
			Notificationsfromadmin.objects.filter(query="Nothing").delete()
		else:
			q=QuerytoAdmin.objects.get(id=query_id)
			created_by = v.ad_name
			created_at = datetime.datetime.now().date()
			modified_by = v.ad_name
			modified_at = datetime.datetime.now().date()
			p = Notificationsfromadmin.objects.create(a_id_id=z,query="Nothing",s_id=student_id,subject=q.subject,created_at= created_at,created_by = created_by,modified_at= modified_at,modified_by= modified_by)
			p.save()
		
		
		
		template = loader.get_template('its/adminanswerqueries.html')
		
		context = {
			'current' : v 
		}	
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')
def adminevents(request):
	if(request.session.get("aid",False)!=False):
		z=logged3.objects.all()[0].aid
		v=college_admin.objects.get(a_id=z)
		all_events = Events.objects.all()
		template = loader.get_template('its/adminevents.html')
		context = {
			'current' : {'all_events' : all_events, 'v': v} 
		}	
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')	
def adminfaculty(request):
	if(request.session.get("aid",False)!=False):
		z=logged3.objects.all()[0].aid
		v=college_admin.objects.get(a_id=z)
		all_faculty = faculty.objects.all()
		template = loader.get_template('its/adminfaculty.html')
		context = {
			'current' : {'all_faculty' : all_faculty, 'v': v} 
		}	
		return HttpResponse(template.render(context,request))	
	else:
		return redirect('homepage')


def adminqueries(request):
	if(request.session.get("aid",False)!=False):
		z=logged3.objects.all()[0].aid
		v=college_admin.objects.get(a_id=z)
		all_queries = v.querytoadmin_set.all()
		#print('retrieved')
		template = loader.get_template('its/adminqueries.html')
		context = {
				'current' : {'admin_queries' : all_queries, 'v': v} 
			}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')

def adminstudents(request):
	if(request.session.get("aid",False)!=False):
		z=logged3.objects.all()[0].aid
		v=college_admin.objects.get(a_id=z)
		all_students = student.objects.all()
		template = loader.get_template('its/adminstudents.html')
		context = {
			'current' : {'all_students' : all_students, 'v': v} 
			}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')	
def authenticate(token):
	url = "https://serene-wildwood-35121.herokuapp.com/oauth/getDetails"
	Payload = {'token' : token,'secret' : "32b29bfed559049a7cb82c01088b3c07759d820dfb99e43a2ecf9ef31baf31e5645679e9f99966f7911117e149fce474d2591b87da6f9f0464780853b6aea652"} 
	k = requests.post(url,Payload)
	
	details = json.loads(k.content.decode('utf-8'))
	#print(details)	
	return details

def callback(request,token):
	info = authenticate(token)
	template = loader.get_template('its/studenthome.html')
	student_data = info['student']
	student_email = student_data[0]['Student_Email']
	s_id = student_data[0]['Id']
	
	if(student.objects.filter(email = student_email).exists() == False):
		new_user = student()
		new_user.s_id = student_data[0]['Id']
		new_user.sroll_no = student_data[0]['Student_ID']
		new_user.first_name = student_data[0]['Student_First_Name']
		new_user.middle_name = student_data[0]['Student_Middle_Name']
		new_user.last_name = student_data[0]['Student_Last_name']
		new_user.dob = getDate(student_data[0]['Student_DOB'][:10])
		new_user.gender = student_data[0]['Student_Gender']
		new_user.mobile = student_data[0]['Student_Mobile']
		new_user.email = student_data[0]['Student_Email']
		new_user.reg_year = int(student_data[0]['Student_Cur_YearofStudy']) - int((student_data[0]['Student_Cur_Sem'])/2)
		r= role.objects.get(role_name = "student")
		new_user.role_id = r
		
		new_user.cur_yos = student_data[0]['Student_Cur_YearofStudy']
		new_user.sem_id = student_data[0]['Student_Cur_Sem']
		new_user.spswd = make_password("iamstudent")
		new_user.save()
	login_user = student.objects.get(email=student_email)
	request.session['id'] = s_id
	request.session['first_name'] = login_user.first_name
	request.session['last_name'] = login_user.last_name
	request.session['email'] = login_user.email
	logged.objects.all().delete()
	u = logged()
	u.sid = login_user.s_id
	u.save()
	s= login_user
	queries_fac = Notificationsfromfaculty.objects.filter(s_id = s.s_id).only('f_id','subject','query')
	queries_from_admin =Notificationsfromadmin.objects.filter(s_id = s.s_id).only('a_id','subject','query')
	template = loader.get_template('its/studenthome.html')
	
	if(queries_fac.count() == 0):
		message="No notifications from faculty"
	else:	
		message = "Notifications"
		
	if(queries_from_admin.count() == 0):
		message1="No notifications from admin"
	else:	
		message1 = "Notifications"
	
	context = {
		'current':s,
		'queries_from_admin':queries_from_admin,
		'queries':queries_fac,
		'message':message,
		'message1':message1,
	}
	if login_user.email == student_email:
		return  HttpResponse(template.render(context,request))	
	
def getDate(s):
	if(s == "0000-00-00"):
		return datetime.date(1998,2,23)
	d = s.split('-')
	year = int(d[0])
	month = int(d[1])
	day = int(d[2])
	return datetime.date(year,month,day)
def adminupdateattendence(request):
	if(request.session.get("aid",False)!=False):
		x=logged3.objects.all()[0].aid
		a = college_admin.objects.get(a_id = x)
		if request.method == 'POST' and request.FILES['myfile']:
			fs = FileSystemStorage()
			myfile = request.FILES['myfile']
			filename = fs.save('attendence/'+ myfile.name, myfile)
			uploaded_file_url = fs.url(filename)
			uploadattendence.objects.create(a_id = a, sheet = uploaded_file_url)
			wb = openpyxl.load_workbook(myfile)
			worksheet = wb["Sheet1"]
			excel_data = list()
			row_data = list()
			for row in worksheet.iter_rows():
				for cell in row:
					row_data.append(cell.value)
				s = student.objects.get(s_id = row_data[0])
				if(row_data[2]=='P'):
					row_data[2]= True
				else:
					row_data[2] = False	
				update = s.attendance_set.create(s_id = s.s_id,c_id = row_data[1],mark = row_data[2],date = row_data[3])
				update.save()
				cur_s = s.s_id
				cur_c = row_data[1]
				t = trackattendence.objects.all()
				if t.filter(s_id = cur_s) and t.filter(c_id = cur_c):
					cur = trackattendence.objects.filter(s_id = cur_s)
					for c in cur:
						if(c.c_id == cur_c):
							c.no_classes = c.no_classes + 1
							if(row_data[2]==True):
								c.present = c.present + 1
							else:
								c.abscent = c.abscent + 1
							c.percent = c.present*100
							c.percent = c.percent / c.no_classes
							c.save()
				else:
					new_entry = trackattendence()
					new_entry.s_id = s
					new_entry.c_id = cur_c
					c = course.objects.get(c_id = cur_c)
					new_entry.course_name = c.course_name
					new_entry.no_classes = 1
					if(row_data[2]==True):
						new_entry.present = 1
						new_entry.abscent = 0
					else:
						new_entry.present = 0
						new_entry.abscent = 1
					new_entry.percent = new_entry.present*100
					new_entry.percent = new_entry.percent / new_entry.no_classes
					new_entry.save()
				row_data = []
		# if request.FILES['myfile'] == False:
		# else:
		# 	alertmessage = "Please Select File"
		# 	context = {
		# 		'current' : a,
		# 		'alertmessage':alertmessage, 
		# 	}
		# 	return render(request,'its/adminupdateattendence.html',context)
		return render(request,'its/adminupdateattendence.html')

	else:
		return redirect('homepage')	

def trackattendance(request):
	if(request.session.get("id",False)!=False):
		x=logged.objects.all()[0].sid
		s=student.objects.get(s_id=x)
		attenddencetrack = trackattendence.objects.filter(s_id = s.s_id)
		context={ 'attenddencetrack' : attenddencetrack,'current':s}
		template = loader.get_template('its/trackattendance.html')
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')	

from django.db.models import Q

def facultyupdateclasses(request):
	if(request.session.get("fid",False)!=False):
		x = logged2.objects.all()[0].fid
		f = faculty.objects.get(f_id = x)
		c = f.course_off
		courses_list = c.split(',')
		d = days.objects.all()
		template = loader.get_template('its/facultyupdateclasses.html')
		context = {
			'courses_list':courses_list,
			'current':f,
			'd': d
		}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')	

def checkslots(request):
	if(request.session.get("fid",False)!=False):
		up = rescheduled.objects.all()
		pd = datetime.datetime.now().date()
		for i in up:
			if(pd > i.date):
				i.delete()
		if request.method=='POST':
			course = request.POST.get('course',False)
			d = request.POST.get('date',False)
			month = datetime.date(int(d[0:4]), int(d[5:7]),int(d[8:10])).strftime('%B')
			string=month+' '+str(d[8:10])+', '+str(d[0:4])
			day=datetime.datetime.strptime(string, '%B %d, %Y').strftime('%A')
			d1 = days.objects.get(day = day).day_id
			name = days.objects.get(day_id = d1)
			s = timetable.objects.filter(day_id = d1 , courses = "NoClass")
			print (s)
			#Entry.objects.filter(~Q(id = 3))
			res = rescheduled.objects.filter(date = d)
			print(res)
			slots = []
			
			for i in s:
				slots.append(i)
			
			for i in s:
				for j in res:
					if(i.timeslots == j.timeslots):
						slots.remove(i)

			print (slots)			

			count = 0
			for i in slots :
				count = count + 1 ; 
			template = loader.get_template('its/updateclasses.html')
			context = { 'slots' : slots, 'name' : name.day, 'course' : course , 'count' : count ,'d' : d }
			return HttpResponse(template.render(context,request))
	else:
		return redirect('homepage')	
def reschedule(request):

	if request.method=='POST':
		s = request.POST.get('slot',False)
		c = request.POST.get('course',False)
		d = request.POST.get('day',False)
		date = request.POST.get('date',False)
		slot=timetable.objects.get(id=s)
		name = days.objects.get(day = d)
		new_entry=rescheduled()
		new_entry.date = date
		new_entry.timeslots = slot.timeslots
		new_entry.day_id = name
		new_entry.courses = c
		new_entry.save()

	return render(request,'its/facultyhome.html')
