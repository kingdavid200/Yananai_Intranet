from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('create/', views.project_create, name='create'),
    path('<uuid:pk>/', views.project_detail, name='detail'),
    path('<uuid:pk>/edit/', views.project_edit, name='edit'),
    path('<uuid:project_pk>/tasks/create/', views.task_create, name='task_create'),
    path('<uuid:project_pk>/tasks/<uuid:task_pk>/edit/', views.task_edit, name='task_edit'),
    path('<uuid:project_pk>/tasks/<uuid:task_pk>/status/', views.task_update_status, name='task_status'),
]
