from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('get_all_list_in_category/<int:category_id>', views.get_all_list_in_category, name='get_all_list_in_category'),
    path('get_all_category', views.get_all_category, name='get_all_category'),
    path('', views.index, name = 'home'),
    path('search_title_in_category', views.search_title_in_category, name='search_title_in_category'),
    path('sort/<int:category_id>', views.sort, name='sort'),
    path('delete_title_from_list', views.delete_title_from_list, name='delete_title_from_list'),
    path('show_all_title_in_category', views.show_all_title_in_category, name='show_all_title_in_category'),
    path('add_original_title_in_category', views.add_original_title_in_category, name='add_original_title_in_category'),
]