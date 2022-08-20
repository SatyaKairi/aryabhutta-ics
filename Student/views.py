from django.http import Http404

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import *
from django.db.models import Q
from .forms import *
# Create your views here.

def Student_create_update_view(request,*args, **kwargs):
    Student=None
    msg = "Create Student"
    Student_id = kwargs.get('id')
    if not Student_id is None:
        Student = Student.objects.get(id=Student_id)
        msg = "Update Student"

    form = StudentCreateForm(request.POST or None,instance=Student)
    if request.POST:
        if form.is_valid():
            Student =form.instance
            Student.user = request.user
            form.save()
            # if student don't have any course selected then redirect to select cource

            return redirect (form.instance.get_detail_url())             
    context = {
            'form':form,
            'object':Student,
            'msg':msg
        }      
    return render(request,'Student/create.html',context)   
def Student_deactivate_view(request):
    if request.POST:
        id = request.POST.get('Student_id')
        Student = Student.objects.get(id=id)
        Student.is_active = False
        Student.modified_by = request.user
        Student.save()
        return redirect('Student:list_view')

def Student_detail_view(request,id,*args, **kwargs):
    student = get_object_or_404(Student,id=id,is_active = True)
    if student:
        course = StudentCourse.objects.filter(student_id = student.id)
        
    context ={
        'object':student,
        'courses': course,

    }
    
    return render(request,'Student/detail.html',context)


def Student_list_view(request,*args, **kwargs):
    q= request.GET.get('q')
    qs = Student.objects.get_all_active_Students()
    if not q is None:
  #TODO: add search Parameters below:
        search_param =  Q(name__icontains =q )| Q( dob__icontains = q)
        qs = qs.filter(search_param)
    context ={
        'object_list': qs
    }
    return render(request,'Student/list.html',context)

def student_course_create_update_view(request,*args, **kwargs):
    course_name=None
    msg = "Select Course"
    form = StudentCourseCreateForm(request.POST or None)
   

    if request.POST:
        if form.is_valid():
            Student_id = kwargs.get('id')
            if not Student_id is None:
                student = Student.objects.get(id=Student_id)
            student_course  =form.instance
            student_course.student = student
            form.save()
            return redirect(student.get_detail_url())

            # return redirect (form.instance.get_detail_url())             
    context = {
            'form':form,
            'msg':msg
        }
    return render(request,'Student/student_course/create.html',context)   

