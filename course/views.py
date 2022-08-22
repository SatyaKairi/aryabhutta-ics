from django.http import Http404

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import *
from django.db.models import Q
from .forms import *
from payments.models import Transaction
import datetime

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
    params = Q(course_id = course.id ) & Q(made_by_id = request.user.id) & Q(status = "TXN_SUCCESS")
    obj = Transaction.objects.filter(params)
    installments = {
        'first_installment':None,
        'second_installment':None,
        'third_installment':None
    }
    paid_on = {
        'first_installment':None,
        'second_installment':None,
        'third_installment':None
    }
    if obj.count() > 0:
        for ob in obj:
            if ob.status =="TXN_SUCCESS":
                installments[ob.installment] = "Paid"
                paid_on[ob.installment] = ob.made_on.strftime('%d/%m/%Y')

        print(paid_on)


        print (installments)
    else:
        print ("no transaction")
    if course:
        total_fee = course.first_installment + course.second_installment + course.third_installment
    context ={
        'object':course,
        'total_fee': total_fee,
        'installments':installments,
        'paid_on':paid_on
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
