from django.http import Http404

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import *
from django.db.models import Q
from .forms import *
# Create your views here.

def Course_create_update_view(request,*args, **kwargs):
    Course=None
    msg = "Create Course"
    Course_id = kwargs.get('id')
    if not Course_id is None:
        Course = Course.objects.get(id=Course_id)
        msg = "Update Course"

    form = CourseCreateForm(request.POST or None,instance=Course)
    if request.POST:
        if form.is_valid():
            Course =form.instance
            Course.user = request.user
            form.save()
            return redirect (form.instance.get_detail_url())             
    context = {
            'form':form,
            'object':Course,
            'msg':msg

        }      
    return render(request,'Course/create.html',context)   
def Course_deactivate_view(request):
    if request.POST:
        id = request.POST.get('Course_id')
        Course = Course.objects.get(id=id)
        Course.is_active = False
        Course.modified_by = request.user
        Course.save()
        return redirect('Course:list_view')

def Course_detail_view(request,id,*args, **kwargs):
    course = get_object_or_404(Course,id=id,is_active = True)
 
    context ={
        'object':course,
    }
    
    return render(request,'Course/detail.html',context)


def Course_list_view(request,*args, **kwargs):
    q= request.GET.get('q')
    qs = Course.objects.get_all_active_Courses()
    if not q is None:
  #TODO: add search Parameters below:
        search_param =  Q(name__icontains =q )| Q( eligibility__icontains = q)
        qs = qs.filter(search_param)
    context ={
        'object_list': qs
    }
    return render(request,'Course/list.html',context)
