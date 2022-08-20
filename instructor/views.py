from django.http import Http404

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import *
from django.db.models import Q
from .forms import *
# Create your views here.

def Instructor_create_update_view(request,*args, **kwargs):
    Instructor=None
    msg = "Create Instructor"
    Instructor_id = kwargs.get('id')
    if not Instructor_id is None:
        Instructor = Instructor.objects.get(id=Instructor_id)
        msg = "Update Instructor"

    form = InstructorCreateForm(request.POST or None,instance=Instructor)
    if request.POST:
        if form.is_valid():
            Instructor =form.instance
            Instructor.user = request.user
            form.save()
            return redirect (form.instance.get_detail_url())             
    context = {
            'form':form,
            'object':Instructor,
            'msg':msg

        }      
    return render(request,'Instructor/create.html',context)   
def Instructor_deactivate_view(request):
    if request.POST:
        id = request.POST.get('Instructor_id')
        Instructor = Instructor.objects.get(id=id)
        Instructor.is_active = False
        Instructor.modified_by = request.user
        Instructor.save()
        return redirect('Instructor:list_view')

def Instructor_detail_view(request,id,*args, **kwargs):
    instructor = get_object_or_404(Instructor,id=id,is_active = True)
 
    context ={
        'object':instructor,
    }
    
    return render(request,'Instructor/detail.html',context)


def Instructor_list_view(request,*args, **kwargs):
    q= request.GET.get('q')
    qs = Instructor.objects.get_all_active_Instructors()
    if not q is None:
  #TODO: add search Parameters below:
        search_param =  Q(name__icontains =q )| Q( experience__icontains = q)
        qs = qs.filter(search_param)
    context ={
        'object_list': qs
    }
    return render(request,'Instructor/list.html',context)
