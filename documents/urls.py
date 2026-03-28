from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_list, name='list'),
    path('upload/', views.document_upload, name='upload'),
    path('<uuid:pk>/download/', views.document_download, name='download'),
    path('<uuid:pk>/delete/', views.document_delete, name='delete'),
]
