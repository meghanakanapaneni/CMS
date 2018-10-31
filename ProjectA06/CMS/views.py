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


# Create your views here.
def dashboard(request):
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
    return render(request,'its/studenthome.html')

def studentlogin(request):
    return render(request,'its/studentlogin.html')

def trackattendance(request):
	x=logged.objects.all()[0].sid
	s=student.objects.get(s_id=x)
	y = get_list_or_404(Attendance,s_id=s)
	#print("dfssgsfg")
	print(y)
	template = loader.get_template('its/trackattendance.html')
	context = {
    	'y':y,
    }
	return HttpResponse(template.render(context,request))
    
def trackacademicprogress(request):
    return render(request,'its/trackacademicprogress.html')
def teaching(request):
    return render(request,'its/teaching.html')
def talks(request):
    return render(request,'its/talks.html')
def login2(request):
	if request.method=='POST':
		try:
			x = faculty.objects.get(froll_no=request.POST['froll_no'])
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


def answerqueries(request):
    return render(request,'its/answerqueries.html')

def details(request):
    return render(request,'its/details.html')

def studentleave(request):
	
	
	x=logged.objects.all()[0].sid
	s=student.objects.get(s_id=x)
	
	if request.method=='POST':
		name = request.POST.get('name', False)
		leave_roll_no = request.POST.get('leave_roll_no', False)
		reason = request.POST.get('reason', False)
		leave_from = request.POST.get('leave_from', False)
		leave_to = request.POST.get('leave_to', False)
		no_ofdays = request.POST.get('no_ofdays', False)
		email = request.POST.get('email',False)
		p = Leave.objects.create(s_id=s,name=name,leave_roll_no=leave_roll_no,reason=reason,leave_from=leave_from,leave_to=leave_to,no_ofdays=no_ofdays,email=email)
		p.save()	
	return render(request,'its/studentleave.html')

def leavesubmit(request):
	return render(request,'its/leavesubmit.html')
def studentprofile(request):
	return render(request,'its/studentprofile.html')
def facultyhome(request):
    return render(request,'its/facultyhome.html')

def facultylogin(request):
    return render(request,'its/facultylogin.html')

def postanswers(request):
    return render(request,'its/postanswers.html')

def queries(request):
    return render(request,'its/queries.html')

def register(request):
    return render(request,'its/register.html')

def talks(request):
    return render(request,'its/talks.html')

def talking(request):
    return render(request,'its/talking.html')

def adminmakequery(request):
    return render(request,'its/adminmakequery.html')

def facultymakequery(request):
    return render(request,'its/facultymakequery.html')


def login3(request):
	if request.method=='POST':
		try:
			x = adm.objects.get(aroll_no=request.POST['aroll_no'])
		except(KeyError,adm.DoesNotExist):
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




def adminhome(request):
    return render(request,'its/adminhome.html')

def addevents(request):
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
	if request.method=='POST':
		f = faculty.objects.count()
		fac_name = request.POST.get('fac_name', False)
		froll_no = request.POST.get('froll_no', False)
		ph_no = request.POST.get('ph_no', False)
		course_off = request.POST.get('course_off', False)
		description = request.POST.get('description', False)
		role_id_id = request.POST.get('role_id_id', False)
		fpswd = request.POST.get('fpswd', False)
		p = faculty.objects.create(f_id=f+1,fac_name=fac_name,froll_no=froll_no,ph_no=ph_no,course_off=course_off,description=description,role_id_id=role_id_id,fpswd=fpswd)
		p.save()		
		return HttpResponse("Successfully saved")
	return render(request,'its/addfaculty.html')


def addstudent(request):
	if request.method=='POST':
		s = student.objects.count()
		first_name = request.POST.get('first_name', False)
		last_name = request.POST.get('last_name', False)
		sroll_no = request.POST.get('sroll_no', False)
		dob = request.POST.get('dob', False)
		gender = request.POST.get('gender', False)
		mobile = request.POST.get('mobile', False)
		spswd = request.POST.get('spswd', False)
		email = request.POST.get('email', False)
		role_id_id = request.POST.get('role_id_id', False)
		sem_id = request.POST.get('sem_id', False)
		cur_yos = request.POST.get('cur_yos', False)
		reg_year = request.POST.get('reg_year', False)
		p = student.objects.create(s_id=s+1,first_name=first_name,last_name=last_name,sroll_no=sroll_no,dob=dob,gender=gender,mobile=mobile,spswd=spswd,email=email,role_id_id=role_id_id,sem_id=sem_id,cur_yos=cur_yos,reg_year=reg_year)
		p.save()		
		return HttpResponse("Successfully saved")
	return render(request,'its/addstudent.html')
	
def adminanswerqueries(request):
	
	if request.method=='POST':
		query = request.POST.get('query', False)
		s_id = request.POST.get('s_id', False)
		a_id = request.POST.get('a_id', False)
		
		a = Answerqueryadmin.objects.create(s_id=s_id,query=query,a_id=a_id)
		a.save()	
	return render(request,'its/adminanswerqueries.html')

def adminevents(request):
    return render(request,'its/adminevents.html')

def adminfaculty(request):
    return render(request,'its/adminfaculty.html')

def adminprofile(request):
    return render(request,'its/adminprofile.html')

def adminlogin(request):
    return render(request,'its/adminlogin.html')



def adminqueries(request):
    all_queries = Query.objects.all()
    template = loader.get_template('its/adminqueries.html')
    context = {
    	'all_queries':all_queries,
    }
    return HttpResponse(template.render(context,request))
    
    

   # return render(request,'its/adminqueries.html')

def teachingcourse(request):
	return render(request,'its/Teaching/IR.html')


def adminstudents(request):
    return render(request,'its/adminstudents.html')
def callback(request,token):
	info = authenticate(token)
	template = loader.get_template('its/studenthome.html')
	context = {
		'data' : info['student'],
	}
	return HttpResponse(template.render(context,request))

def authenticate(token):
	url = "https://serene-wildwood-35121.herokuapp.com/oauth/5bd892288e583700150e4dd5"
	Payload = {'token' : token,'secret' : "32b29bfed559049a7cb82c01088b3c07759d820dfb99e43a2ecf9ef31baf31e5645679e9f99966f7911117e149fce474d2591b87da6f9f0464780853b6aea652"} 
	k = requests.post(url,Payload)
	details = json.loads(k.content)
	print(details)
	return details
