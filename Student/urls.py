
from django.urls import path
from .views import *
app_name = "student"
urlpatterns =[

    path('', Student_list_view, name='list_view' ),
    
    path('create/',Student_create_update_view, name = 'create_view'),
    path('<id>/update/',Student_create_update_view, name = 'update_view'),
    path('deactivate/',Student_deactivate_view, name = 'deactivate_view'),
    path('<id>/',Student_detail_view, name = 'detail_view'),
    path('<id>/course_create/',student_course_create_update_view, name = 'course_create_view'),
]
