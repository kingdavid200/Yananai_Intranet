from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='list'),
    path('create/', views.news_create, name='create'),
    path('<uuid:pk>/', views.news_detail, name='detail'),
    path('<uuid:pk>/edit/', views.news_edit, name='edit'),
    path('<uuid:pk>/delete/', views.news_delete, name='delete'),
]
