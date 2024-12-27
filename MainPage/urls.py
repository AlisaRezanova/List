from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('get_all_list_in_category/<int:category_id>', views.get_all_list_in_category, name='get_all_list_in_category'),
    path('get_all_category', views.get_all_category, name='get_all_category'),
    path('', views.index, name = 'home'),
]