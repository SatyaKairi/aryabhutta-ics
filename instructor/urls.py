
from django.urls import path
from .views import *
app_name = "instructor"
urlpatterns =[

    path('', Instructor_list_view, name='list_view' ),
    
    path('create/',Instructor_create_update_view, name = 'create_view'),
    path('<id>/update/',Instructor_create_update_view, name = 'update_view'),
    path('deactivate/',Instructor_deactivate_view, name = 'deactivate_view'),
    
    path('<id>/',Instructor_detail_view, name = 'detail_view'),


    
]
