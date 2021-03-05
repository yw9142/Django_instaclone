from django.urls import path
from .views import *

app_name = 'post'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('new/', post_new, name='post_new'),  # 새 포스트 작성 url
    path('edit/<int:pk>/', post_edit, name='post_edit'),  # <int:pk> 키값.
    path('delete/<int:pk>/', post_delete, name='post_delete'),
]
