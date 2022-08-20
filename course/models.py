from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

class CourseManager(models.Manager):
    def get_all_active_Courses(self):
        return Course.objects.filter(is_active = True)

class Course(models.Model):
    name=models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField()
    eligibility=models.CharField(max_length=100)
    duration=models.DecimalField(max_digits=10, decimal_places=2)
    first_installment = models.DecimalField(max_digits=10, decimal_places=2)
    second_installment = models.DecimalField(max_digits=10, decimal_places=2)
    third_installment = models.DecimalField(max_digits=10, decimal_places=2)
    start_date=models.DateTimeField(auto_now=False)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank = True, related_name="modified_Course_user")
    is_active = models.BooleanField(default=True)
    objects=CourseManager()

    def __str__(self):
        return self.name
# Urls
    def get_detail_url(self,**kwargs):
        return reverse ('course:detail_view', kwargs={'id' :self.id})
    def get_update_url(self,**kwargs):
        return reverse ('course:update_view', kwargs={'id' :self.id})
