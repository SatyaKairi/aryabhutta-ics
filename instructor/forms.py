from dataclasses import fields
from django import forms
from .models import Instructor

class InstructorCreateForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['name','experience','phone_no','address']
       
        
        
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(
                {
            'placeholder': f'{str(field)}',
            'class': 'form-control'
            }
                
        )
    
