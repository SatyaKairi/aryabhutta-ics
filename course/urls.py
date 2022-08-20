
from django.urls import path
from .views import *
app_name = "course"
urlpatterns =[

    path('', Course_list_view, name='list_view' ),
    path('create/',Course_create_update_view, name = 'create_view'),
    path('<id>/update/',Course_create_update_view, name = 'update_view'),
    path('deactivate/',Course_deactivate_view, name = 'deactivate_view'),
    path('<id>/',Course_detail_view, name = 'detail_view'),
    
]
