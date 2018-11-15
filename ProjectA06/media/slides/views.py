# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.contrib.auth.hashers import make_password, check_password
import requests
from .models import course, user, topic, subtopic, question_type, level, exam_detail, question_bank,  option, answer, registration, result

def faculty_dashboard(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        return render(request ,'online_exam/faculty_dashboard.html')
    else:
        return redirect("../login")

@csrf_exempt
def faculty_add_course(srequest):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        if request.method=="POST":
            temp = course()
            temp.course_name = request.POST['course_name']
            temp.description = request.POST['description']
            temp.faculty = request.POST['faculty']
            print(temp)
            if(course.objects.filter(course_name=temp.course_name).count() == 0):
                temp.save()
                message = "Course was successfully added!!"
                return render(request ,'online_exam/faculty_add_course.html',{"message":message})
            else:
                wrong_message = "Sorry, course already exists!!"
                return render(request,'online_exam/faculty_add_course.html',{"wrong_message":wrong_message})
        else:
            return render(request,'online_exam/faculty_add_course.html')
    else:
        return redirect("../login")

@csrf_exempt
def faculty_add_exam(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        if(request.POST.get('exam_name', False) != False and request.POST.get('description', False) != False and request.POST.get('course_id', False) != False and request.POST.get('year', False) != False and request.POST.get('status', False) != False and request.POST.get('startDate', False) != False and request.POST.get('endDate', False) != False and request.POST.get('startTime', False) != False and request.POST.get('endTime', False) != False and request.POST.get('pass_percentage', False) != False and request.POST.get('no_of_questions', False) != False and request.POST.get('attempts_allowed', False) != False):
            temp = exam_detail()
            temp.exam_name = request.POST['exam_name']
            temp.description = request.POST['description']
            temp.course_id = course.objects.get(id=request.POST['course_id'])
            temp.year = request.POST['year']
            temp.status = request.POST['status']
            temp.start_time = request.POST['startDate']+" "+request.POST['startTime']
            temp.end_time = request.POST['endDate']+" "+request.POST['endTime']
            temp.pass_percentage = request.POST['pass_percentage']
            temp.no_of_questions = request.POST['no_of_questions']
            temp.attempts_allowed = request.POST['attempts_allowed']
            if(exam_detail.objects.filter(exam_name=temp.exam_name).count() == 0):
                temp.save()
                print("saved")
                message = "Examination was successfully added!"
                return render(request ,'online_exam/faculty_add_exam.html', {"message":message})
            else:
                wrong_message = "Sorry, exam already exists!"
                return render(request ,'online_exam/faculty_add_exam.html', {"wrong_message":wrong_message})
        else:
            print("else entered")
            return render(request ,'online_exam/faculty_add_exam.html', {"courses":course.objects.all()})
    else:
        return redirect("../login")

def faculty_add_topic(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        if(request.POST.get('topic_name', False) != False and request.POST.get('status', False) != False and request.POST.get('description', False) != False):
            temp = topic()
            temp.topic_name = request.POST['topic_name']
            temp.description = request.POST['description']
            temp.status = request.POST['status']
            if(topic.objects.filter(topic_name=temp.topic_name).count() == 0):
                temp.save()
                message = "Topic was successfully added!!"
                return render(request ,'online_exam/faculty_add_topic.html', {"message":message})
            else:
                wrong_message = "Sorry, topic already exists!!"
                return render(request ,'online_exam/faculty_add_topic.html', {"wrong_message":wrong_message})
        else:
            return render(request ,'online_exam/faculty_add_topic.html')
    else:
        return redirect("../login")

def faculty_add_subtopic(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        if(request.POST.get('subtopic_name', False) != False and request.POST.get('status', False) != False and request.POST.get('description', False) != False and request.POST.get('topic_id', False) != False):
            temp = subtopic()
            temp.subtopic_name = request.POST['subtopic_name']
            temp.description = request.POST['description']
            temp.status = request.POST['status']
            temp.topic_id = topic.objects.get(id=request.POST['topic_id'])
            if(subtopic.objects.filter(subtopic_name=temp.subtopic_name).count() == 0):
                temp.save()
                message = "Subtopic was successfully added!!"
                return render(request ,'online_exam/faculty_add_subtopic.html',  {"topics":topic.objects.all(),"message":message})
            else:
                wrong_message = "Sorry, subtopic already exists!!"
                return render(request ,'online_exam/faculty_add_subtopic.html',  {"topics":topic.objects.all(),"wrong_message":wrong_message})
        else:
            return render(request ,'online_exam/faculty_add_subtopic.html', {"topics":topic.objects.all()})
    else:
        return redirect("../login")
def faculty_add_question(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        return render(request ,'online_exam/faculty_add_question.html', {"courses": course.objects.all(), "topics": topic.objects.all(), "levels": level.objects.all(), "question_type":question_type.objects.all()})
    else:
        return redirect("../login")

@csrf_exempt
def faculty_modify_course(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        if request.method=="POST":
            temp = course()
            temp.course_id = request.POST['id']
            temp.course_name = request.POST['course_name']
            temp.description = request.POST['description']
            temp.status = request.POST['status']
            if(course.objects.filter(course_name=temp.course_name).count() == 0 ):
                course.objects.filter(id=temp.course_id).update(course_name=temp.course_name, description = temp.description, status = temp.status, modified = datetime.datetime.now())
                message = "Course was updated successfully!!"
                return render(request ,'online_exam/faculty_modify_course.html', {"courses":course.objects.all(),"message":message})
            elif(course.objects.filter(course_name = temp.course_name).count() == 1 and list(course.objects.filter(course_name=temp.course_name).values("id"))[0]['id'] == int(request.POST['id'])):
                course.objects.filter(id=temp.course_id).update(course_name=temp.course_name, description = temp.description, status = temp.status, modified = datetime.datetime.now())
                message = "Course was updated successfully!!"
                return render(request ,'online_exam/faculty_modify_course.html', {"courses":course.objects.all(),"message":message})
            else:
                wrong_message = "Sorry, the course already exists!!"
                return render(request ,'online_exam/faculty_modify_course.html', {"courses":course.objects.all(),"wrong_message":wrong_message})
        else:
            return render(request ,'online_exam/faculty_modify_course.html', {"courses":course.objects.all()})
    else:
        return redirect("../login")

@csrf_exempt
def faculty_modify_exam(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        print("entered")
        print("id---------------------------------------------------------", request.POST.get('id'))
        if(request.POST.get('id', False) != False and request.POST.get('exam_name', False) != False and request.POST.get('exam_name', False) != False and request.POST.get('description', False) != False and request.POST.get('course_id', False) != False and request.POST.get('year', False) != False and request.POST.get('status', False) != False and request.POST.get('startDate', False) != False and request.POST.get('endDate', False) != False and request.POST.get('startTime', False) != False and request.POST.get('endTime', False) != False and request.POST.get('pass_percentage', False) != False and request.POST.get('no_of_questions', False) != False and request.POST.get('attempts_allowed', False) != False):
            #if request.method == 'POST':
            temp = exam_detail()
            print("if entered")
            temp.id = request.POST['id']
            temp.exam_name = request.POST['exam_name']
            temp.description = request.POST['description']
            temp.course_id = course.objects.get(course_name=request.POST['course_id'])
            temp.year = request.POST['year']
            temp.status = request.POST['status']
            temp.start_time = request.POST['startDate']+" "+request.POST['startTime']
            temp.end_time = request.POST['endDate']+" "+request.POST['endTime']
            temp.pass_percentage = request.POST['pass_percentage']
            temp.no_of_questions = request.POST['no_of_questions']
            temp.attempts_allowed = request.POST['attempts_allowed']
            if(exam_detail.objects.filter(exam_name=temp.exam_name).count() == 0):
                exam_detail.objects.filter(id=temp.id).update(exam_name=temp.exam_name, description=temp.description, course_id=temp.course_id, year=temp.year, status=temp.status, start_time=temp.start_time, end_time=temp.end_time, pass_percentage=temp.pass_percentage, no_of_questions=temp.no_of_questions, attempts_allowed=temp.attempts_allowed, modified=datetime.datetime.now())
                print("saved")
                message = "Examination was successfully updated!"
                return render(request ,'online_exam/faculty_modify_exam.html', {"message":message, "exams": exam_detail.objects.all()})
            else:
                wrong_message = "Sorry, exam already exists!"
                return render(request ,'online_exam/faculty_modify_exam.html', {"wrong_message":wrong_message, "exams": exam_detail.objects.all()})
        else:
            print("else entered")
            return render(request ,'online_exam/faculty_modify_exam.html', {"exams":exam_detail.objects.all()})
    else:
        return redirect("../login")
def faculty_modify_topic(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        if(request.POST.get('id', False) != False and request.POST.get('topic_name', False) != False and request.POST.get('status', False) != False and request.POST.get('description', False) != False):
            temp = topic()
            temp.topic_id = request.POST['id']
            temp.topic_name = request.POST['topic_name']
            temp.description = request.POST['description']
            temp.status = request.POST['status']
            if(topic.objects.filter(topic_name=temp.topic_name).count() == 0 ):
                topic.objects.filter(id=temp.topic_id).update(topic_name=temp.topic_name, description = temp.description, status = temp.status, modified = datetime.datetime.now())
                message = "Topic was updated successfully!!"
                return render(request ,'online_exam/faculty_modify_topic.html', {"topics":topic.objects.all(),"message":message})
            elif(topic.objects.filter(topic_name = temp.topic_name).count() == 1 and list(topic.objects.filter(topic_name=temp.topic_name).values("id"))[0]['id'] == int(request.POST['id'])):
                topic.objects.filter(id=temp.topic_id).update(topic_name=temp.topic_name, description = temp.description, status = temp.status, modified = datetime.datetime.now())
                message = "Topic was updated successfully!!"
                return render(request ,'online_exam/faculty_modify_topic.html', {"topics":topic.objects.all(),"message":message})
            else:
                wrong_message = "Sorry, the topic already exists!!"
                return render(request ,'online_exam/faculty_modify_topic.html', {"topics":topic.objects.all(),"wrong_message":wrong_message})
        else:
            return render(request ,'online_exam/faculty_modify_topic.html', {"topics":topic.objects.all()})
    else:
        return redirect("../login")

def faculty_modify_subtopic(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        if(request.POST.get('id', False) != False and request.POST.get('subtopic_name', False) != False and request.POST.get('status', False) != False and request.POST.get('description', False) != False and request.POST.get('topic_id', False) != False):
            temp = subtopic()
            temp.subtopic_id = request.POST['id']
            temp.subtopic_name = request.POST['subtopic_name']
            temp.description = request.POST['description']
            temp.status = request.POST['status']
            temp.topic_id = topic.objects.get(id=request.POST['topic_id'])
            if(subtopic.objects.filter(subtopic_name=temp.subtopic_name, topic_id = temp.topic_id).count() == 0 ):
                subtopic.objects.filter(id=temp.subtopic_id).update(subtopic_name=temp.subtopic_name, description = temp.description, topic_id =temp.topic_id, status = temp.status, modified = datetime.datetime.now())
                message = "SubTopic was updated successfully!!"
                return render(request ,'online_exam/faculty_modify_subtopic.html', {"subtopics":subtopic.objects.all(),"topics":topic.objects.all(),"message":message})
            elif(subtopic.objects.filter(subtopic_name=temp.subtopic_name, topic_id = temp.topic_id).count() == 1 and list(subtopic.objects.filter(subtopic_name=temp.subtopic_name, topic_id = temp.topic_id).values("id"))[0]['id'] == int(request.POST['id'])):
                subtopic.objects.filter(id=temp.subtopic_id).update(subtopic_name=temp.subtopic_name, description = temp.description, topic_id =temp.topic_id, status = temp.status, modified = datetime.datetime.now())
                message = "SubTopic was updated successfully!!"
                return render(request ,'online_exam/faculty_modify_subtopic.html', {"subtopics":subtopic.objects.all(),"topics":topic.objects.all(),"message":message})
            else:
                wrong_message = "Sorry, the subtopic already exists!!"
                return render(request ,'online_exam/faculty_modify_subtopic.html', {"subtopics":subtopic.objects.all(),"topics":topic.objects.all(),"wrong_message":wrong_message})
        else:
            return render(request ,'online_exam/faculty_modify_subtopic.html', {"subtopics":subtopic.objects.all(),"topics":topic.objects.all()})
    else:
        return redirect("../login")

def faculty_modify_question(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        return render(request ,'online_exam/faculty_modify_question.html')
    else:
        return redirect("../login")

@csrf_exempt
def faculty_update_course(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        if request.method=="POST":
            ID = request.POST['id']
            print(ID)
            data = course.objects.get(pk = int(request.POST['id']))
            return render(request ,'online_exam/faculty_update_course.html', {"data": data})
    else:
        return redirect("../login")

@csrf_exempt
def faculty_update_exam(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        result = exam_detail.objects.get(pk= int(request.POST['id']))
        return render(request ,'online_exam/faculty_update_exam.html', {"result": result, "courses":course.objects.all()})
        #print("id---------------------------------------------------------", int(request.POST['id']))
    else:
        return redirect("../login")

def faculty_update_topic(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        result = topic.objects.get(pk = int(request.POST['id']))
        return render(request ,'online_exam/faculty_update_topic.html', {"result": result})
    else:
        return redirect("../login")

def faculty_update_subtopic(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        result = subtopic.objects.get(pk = int(request.POST['id']))
        print(result.topic_id.topic_name)
        return render(request ,'online_exam/faculty_update_subtopic.html', {"result":result, "topics":topic.objects.all()})
    else:
        return redirect("../login")

def faculty_update_question(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        return render(request ,'online_exam/faculty_update_question.html')
    else:
        return redirect("../login")

def faculty_view_courses(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        return render(request ,'online_exam/faculty_view_courses.html', {"courses":course.objects.all()})
    else:
        return redirect("../login")

@csrf_exempt
def faculty_view_exams(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        data = exam_detail.objects.all()
        #print(data)
        return render(request ,'online_exam/faculty_view_exams.html', {"exams":exam_detail.objects.all()})
    else:
        return redirect("../login")

def faculty_view_topics(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        return render(request ,'online_exam/faculty_view_topics.html', {"topics":topic.objects.all()})
    else:
        return redirect("../login")

def faculty_view_subtopics(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        L=[]
        for i in subtopic.objects.all():
            K = dict()
            K['subtopic_name'] = i.subtopic_name
            K['description'] = i.description
            K['created'] = i.created
            K['modified'] = i.modified
            K['status'] = i.status
            K['topic_name'] = ((i.topic_id).topic_name)
            L.append(K)
        return render(request ,'online_exam/faculty_view_subtopics.html', {"subtopics":L})
    else:
        return redirect("../login")

def faculty_view_questions(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        V=[]
        for i in question_bank.objects.all():
            A = dict()
            A['question'] = i.question
            A['description'] = i.description
            A['question_type'] = i.question_type.q_type
            A['subtopic'] = i.subtopic_id.subtopic_name
            A['level'] = i.level_id.level_name
            A['exam'] = i.exam_id.exam_name
            A['score'] = i.score
            A['created'] = i.created
            A['modified'] = i.modified
            A['status'] = i.status
            A['topic_name'] = (i.subtopic_id.topic_id.topic_name)
            V.append(A)
        return render(request ,'online_exam/faculty_view_questions.html',{"questions":V})
    else:
        return redirect("../login")

def faculty_evaluate(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        return render(request ,'online_exam/faculty_evaluate.html')
    else:
        return redirect("../login")

def faculty_exam_registrations(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        return render(request ,'online_exam/faculty_exam_registrations.html')
    else:
        return redirect("../login")

def faculty_user_registrations(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        return render(request ,'online_exam/faculty_user_registrations.html')
    else:
        return redirect("../login")

def faculty_profile(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0):
        return render(request ,'online_exam/faculty_profile.html')
    else:
        return redirect("../login")
# Create your views here.
def student_dashboard(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 1):
        return render(request, 'online_exam/student_dashboard.html')
    else:
        return redirect("../login")

def student_exams(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 1):
        return render(request, 'online_exam/student_exams.html')
    else:
        return redirect("../login")

def student_attempt_exam(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 1):
        questions = question_bank.objects.all()
        K = dict()
        exam_id = ""
        j = 0
        for i in questions:
            L = dict()
            L['question_id'] = i.id
            L['question'] = i.question
            L['question_type'] = i.question_type.q_type
            if(i.question_type.id == 1 or i.question_type.id == 2):
                opt_dict = dict()
                for k in option.objects.filter(question_id = i.id):
                    opt_dict[k.option_no] = k.option_value
                L['options'] = opt_dict
            else:
                L['options'] = ""
            #L['answer'] = dict(answer.objects.filter(question_id = i.id).values("answer"))
            L['level'] = i.level_id.level_name
            L['subtopic'] = i.subtopic_id.subtopic_name
            L['topic'] = i.subtopic_id.topic_id.topic_name
            L['score'] = i.score
            L['exam'] = i.exam_id.exam_name
            exam_id = i.exam_id.id
            L['course'] = i.exam_id.course_id.course_name
            j += 1
            K[j] = L
        final = json.dumps(K)
        return render(request, 'online_exam/student_attempt_exam.html', {"myArray":final, "sizeMyArray":j, "exam_id":exam_id})
    else:
        return redirect("../login")

def student_verify(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 1):
        return HttpResponse("HELLO")
    else:
        return redirect("../login")

def student_progress(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 1):
        return render(request, 'online_exam/student_progress.html')
    else:
        return redirect("../login")

def student_profile(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 1):
        return render(request, 'online_exam/student_profile.html')
    else:
        return redirect("../login")

def login(request):
    if(request.session.get('id', False) == False):
        if(request.method == "POST" and request.POST.get('email', False) != False and request.POST.get('password', False) != False):
            if(user.objects.filter(email = request.POST['email']).exists()):
                login_user = user.objects.get(email = request.POST['email'])
                if (check_password(request.POST.get('password', False),login_user.password) == True):
                    request.session['id'] = login_user.id
                    request.session['first_name'] = login_user.first_name
                    request.session['last_name'] = login_user.last_name
                    request.session['email'] = login_user.email
                    request.session['phone'] = login_user.phone
                    request.session['account_type'] = login_user.account_type
                    return redirect('../login')
                else:
                    return render(request, 'online_exam/Login.html', {"message":"Invalid Credentials!!"})
            else:
                return render(request, 'online_exam/Login.html', {"message":"Invalid Credentials!!"})
        return render(request, 'online_exam/Login.html')
    elif(request.session.get('account_type', False) == 0):
        return redirect("../faculty_dashboard")
    elif(request.session.get('account_type', False) == 1):
        return redirect("../student_dashboard")
    return render(request, 'online_exam/Login.html')

def signup(request):
    if(request.method == "POST" and request.POST.get('first_name', False) != False and request.POST.get('last_name', False) != False and request.POST.get('email', False) != False and request.POST.get('phone', False) != False):
        new_user = user(first_name = request.POST['first_name'], last_name = request.POST['last_name'], phone = request.POST['phone'], email = request.POST['email'], password = make_password(request.POST['password']))
        if(user.objects.filter(email=request.POST['email']).exists()):
            error_message = "Email ID already exists!!"
            return render(request, 'online_exam/Signup.html', {"error_message":error_message})
        else:
            new_user.save()
            message = "Account Created Successfully!!"
            return render(request, 'online_exam/Signup.html', {"message":message})
    return render(request, 'online_exam/Signup.html')

def sign_out(request):
    request.session.flush()
    return redirect('../login')

def authenticate(request, token=None):
    clientSecret = "1c616e2f378f9aa90c936b1560e6d0c372fa5e5a54457356f39573955e7e64b445d2f03673a8905088b43c114465020825f48b79e8ce85b0e20e6ad8b736e860"
    Payload = { 'token': token, 'secret': clientSecret }
    k = requests.post("https://serene-wildwood-35121.herokuapp.com/oauth/getDetails", Payload)
    data = json.loads(k.content) 
    print(data['student'][0]['Student_Email'])
    user_email = data['student'][0]['Student_Email']
    if(user.objects.filter(email=user_email).exists() == False):
        new_user = user()
        new_user.first_name = data['student'][0]['Student_First_Name']
        new_user.last_name = data['student'][0]['Student_Last_name']
        new_user.email = data['student'][0]['Student_Email']
        new_user.phone = data['student'][0]['Student_Mobile']
        new_user.password = make_password("iamstudent")
        new_user.save()
    login_user = user.objects.get(email = user_email)
    request.session['id'] = login_user.id
    request.session['first_name'] = login_user.first_name
    request.session['last_name'] = login_user.last_name
    request.session['email'] = login_user.email
    request.session['phone'] = login_user.phone
    request.session['account_type'] = login_user.account_type
    return redirect('login')

def get_exams_by_course(request):
    if(request.session.get('id', False) != False and request.session.get('account_type', False) == 0 and request.POST.get('course_id', False) != False):
        exams = dict()
        j = 0
        for i in (exam_detail.objects.filter(course_id=course.objects.filter(id = request.POST.get('course_id', False)).all()).values("id", "exam_name")):
            exams[i['id']] = i['exam_name']
            j += 1
        return HttpResponse(json.dumps(exams))
    return HttpResponseNotFound('<h1>Page not found</h1>')