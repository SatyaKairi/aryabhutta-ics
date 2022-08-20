from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from course.models import Course

class StudentManager(models.Manager):
    def get_all_active_Students(self):
        return Student.objects.filter(is_active = True)

class Student(models.Model):
    name=models.CharField(max_length=100)
    dob=models.DateTimeField(auto_now=False)
    standard=models.TextField()
    joining_date=models.DateTimeField(auto_now=False)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank = True, related_name="modified_Student_user")
    is_active = models.BooleanField(default=True)
    objects=StudentManager()

    def __str__(self):
        return self.name
# Urls
    def get_detail_url(self,**kwargs):
        return reverse ('student:detail_view', kwargs={'id' :self.id})
    def get_update_url(self,**kwargs):
        return reverse ('student:update_view', kwargs={'id' :self.id})
    def get_course_url(self,**kwargs):
        return reverse ('student:course_create_view', kwargs={'id' :self.id})
    
class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    #courses = courseManager.get_all_active_courses()
    course = models.ForeignKey(Course,on_delete=models.SET_NULL, blank=True, null=True)
    joining_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student) + ': ' + str(self.course)

