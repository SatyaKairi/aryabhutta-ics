from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

class InstructorManager(models.Manager):
    def get_all_active_Instructors(self):
        return Instructor.objects.filter(is_active = True)

class Instructor(models.Model):
    name=models.CharField(max_length=100)
    experience=models.DecimalField(max_digits=10, decimal_places=2)
    phone_no=models.DecimalField(max_digits=10, decimal_places=2)
    address=models.CharField(max_length=100)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank = True, related_name="modified_Instructor_user")
    is_active = models.BooleanField(default=True)
    objects=InstructorManager()
    
    def __str__(self):
        return self.name
# Urls
    def get_detail_url(self,**kwargs):
        return reverse ('instructor:detail_view', kwargs={'id' :self.id})
    def get_update_url(self,**kwargs):
        return reverse ('instructor:update_view', kwargs={'id' :self.id})
