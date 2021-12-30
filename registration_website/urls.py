from django.contrib import admin
from django.urls import path,include
from registration_website import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('subject/add/', views.subject_form, name='subject_add'),
    path('subject/edit/<int:id>/', views.subject_form, name='subject_update'),
    path('subject/view/<int:id>/', views.subject_view, name='subject_view'),
    path('subject/list/', views.subject_list, name='subject_list'),
    path('school/add/', views.school_form, name='school_add'),
    path('school/edit/<int:id>/', views.school_form, name='school_update'),
    path('school/view/<int:id>/', views.school_view, name='school_view'),
    path('school/list/', views.school_list, name='school_list'),
    path('apply/', views.student_apply, name='registration_apply'),
]