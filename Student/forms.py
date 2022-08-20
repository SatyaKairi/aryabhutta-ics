from dataclasses import fields
from django import forms
from .models import Student, StudentCourse

class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name','dob','standard','joining_date']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(
                {
            'placeholder': f'{str(field)}',
            'class': 'form-control'
            }
                
        )

class StudentCourseCreateForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ['course']
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
    #     for field in self.fields:
    #         self.fields[str(field)].widget.attrs.update(
    #             {
    #         'placeholder': f'{str(field)}',
    #         'class': 'form-control'
    #         }
                
    #     )
    
