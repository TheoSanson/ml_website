from django.contrib import admin
from django.urls import path,include
from registration_website import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('user/dashboard/',views.user_dashboard, name='user_dashboard'),
    path('user/form/',views.user_form, name='user_add'),
    path('user/list/',views.user_list, name='user_list'),
    path('user/view/<int:id>/',views.user_view, name='user_view'),
    path('user/edit/',views.user_edit, name='user_edit'),
    path('user/edit/admin/<int:id>',views.user_admin_edit, name='user_admin_edit'),
    path('user/permission/',views.user_permission_redirect, name='permission_redirect'),
    path('subject/add/', views.subject_form, name='subject_add'),
    path('subject/edit/<int:id>/', views.subject_form, name='subject_update'),
    path('subject/view/<int:id>/', views.subject_view, name='subject_view'),
    path('subject/list/', views.subject_list, name='subject_list'),
    path('school/add/', views.school_form, name='school_add'),
    path('school/edit/<int:id>/', views.school_form, name='school_update'),
    path('school/view/<int:id>/', views.school_view, name='school_view'),
    path('school/list/', views.school_list, name='school_list'),
    path('apply/', views.student_apply, name='registration_apply'),
    path('search/', views.student_search, name='registration_search'),
    path('list/', views.student_list, name='registration_list'),
    path('view/<str:key>/', views.student_view, name='registration_view'),
    path('view/admin/<int:id>/', views.student_admin_view, name='registration_admin_view'),
    path('print/<int:id>/', views.student_print, name='registration_print'),
    path('exam/add/', views.examination_form, name='exam_add'),
    path('exam/update/<int:id>/', views.examination_edit, name='exam_update'),
    path('exam/list/', views.examination_list, name='exam_list'),
    path('exam/view/<int:id>/', views.examination_view, name='exam_view'),
    path('exam/print/<int:id>/', views.examination_print, name='exam_print'),
    path('exam/venue/print/<int:id>/', views.examination_venue_print, name='exam_venue_print'),
    path('college/add/', views.college_venue_form, name='college_add'),
    path('college/edit/<int:id>', views.college_venue_form, name='college_edit'),
    path('college/list/', views.college_list, name='college_list'),
    path('college/view/<int:id>', views.college_view, name='college_view'),
]