from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(role)
admin.site.register(student)
admin.site.register(faculty)
admin.site.register(college_admin)
admin.site.register(course)
admin.site.register(registeredcourses)
admin.site.register(days)
admin.site.register(timetable)
admin.site.register(Grade)
admin.site.register(Attendance)
admin.site.register(uploadattendence)
admin.site.register(trackattendence)
admin.site.register(Leave)
admin.site.register(Query)
admin.site.register(Answerqueryadmin)
admin.site.register(Events)
admin.site.register(QuerytoAdmin)
admin.site.register(UploadSlides)
admin.site.register(Notificationsfromfaculty)
admin.site.register(Notificationsfromadmin)
