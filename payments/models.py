from logging import NullHandler
from django.db import models
from django.contrib.auth import get_user_model
from course.models import Course
# from ..project.models import Project, ProjectContribution

User = get_user_model()

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # installments = (
    #     ('first_installment', 'First Installment'),
    #     ('second_installment', 'Second Installment'),
    #     ('third_installment', 'Third Installment'),
    # )
    installment = models.CharField(max_length=100)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=100, blank=True, null=True)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        print(self.id)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.course.name

