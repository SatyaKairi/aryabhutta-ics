from dataclasses import fields
from django import forms
from .models import Course

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name','eligibility','duration','start_date']
       
        
        
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(
                {
            'placeholder': f'{str(field)}',
            'class': 'form-control'
            }
                
        )
    
