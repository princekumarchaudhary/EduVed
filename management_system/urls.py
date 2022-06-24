"""management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from management_system import settings
from student_management_app import views,Hodview,Staffview,Studentview
urlpatterns = [
    path('home',views.homepage),
    path('admin/', admin.site.urls),
    path('',views.loginpage,name="show_login"),
    path('doLogin', views.doLogin,name="do_login"),
    path('get_user_details',views.get_user_details),
    path('logout_user',views.logout_user,name="logout"),
    path('admin_home',Hodview.admin_home,name="admin_home"),
    path('add_staff',Hodview.add_staff,name="add_staff"),
    path('add_staff_save',Hodview.add_staff_save,name="add_staff_save"),
    path('add_course',Hodview.add_course,name="add_course"),
    path('add_course_save',Hodview.add_course_save,name="add_course_save"),
    path('add_student',Hodview.add_student,name="add_student"),
    path('add_student_save',Hodview.add_student_save,name="add_student_save"),
    path('add_subject',Hodview.add_subject,name="add_subject"),
    path('add_subject_save',Hodview.add_subject_save,name="add_subject_save"),
    path('manage_staff',Hodview.manage_staff,name="manage_staff"),
    path('manage_student',Hodview.manage_student,name="manage_student"),
    path('manage_course',Hodview.manage_course,name="manage_course"),
    path('manage_subject',Hodview.manage_subject,name="manage_subject"),
    path('edit_staff/<staff_id>/',Hodview.edit_staff,name="edit_staff"),
    path('edit_staff_save',Hodview.edit_staff_save,name="edit_staff_save"),
    path('edit_student/<student_id>',Hodview.edit_student,name="edit_student"),
    path('edit_student_save',Hodview.edit_student_save,name="edit_student_save"),
    path('edit_subject/<subject_id>',Hodview.edit_subject,name="edit_subject"),
    path('edit_subject_save',Hodview.edit_subject_save,name="edit_subject_save"),
    path('edit_course/<course_id>',Hodview.edit_course,name="edit_course"),
    path('edit_course_save',Hodview.edit_course_save,name="edit_course_save"),
    path('check_email_exist',Hodview.check_email_exist,name="check_email_exist"),
    path('check_username_exist', Hodview.check_username_exist, name="check_username_exist"),
    path('admin_view_attendance', Hodview.admin_view_attendance, name="admin_view_attendance"),
    path('admin_get_attendance_dates', Hodview.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    path('admin_get_attendance_student', Hodview.admin_get_attendance_student, name="admin_get_attendance_student"),



    path('staff_home',Staffview.staff_home,name="staff_home"),
    path('staff_taken_attendance',Staffview.staff_taken_attendance,name="staff_taken_attendance"),
    path('staff_update_attendance',Staffview.staff_update_attendance,name="staff_update_attendance"),
    path('get_students',Staffview.get_students,name="get_students"),
    path('get_attendance_dates',Staffview.get_attendance_dates,name="get_attendance_dates"),
    path('get_attendance_student',Staffview.get_attendance_student,name="get_attendance_student"),
    path('save_attendance_data',Staffview.save_attendance_data,name="save_attendance_data"),
    path('update_attendance_data',Staffview.update_attendance_data, name="update_attendance_data"),
    path('add_student_staff',Staffview.add_student_staff,name="add_student_staff"),
    path('add_student_save_staff',Staffview.add_student_save_staff,name="add_student_save_staff"),
    path('manage_student_staff',Staffview.manage_student_staff,name="manage_student_staff"),
    path('edit_student_staff/<student_id>',Staffview.edit_student_staff,name="edit_student_staff"),
    path('edit_student_save_staff',Staffview.edit_student_save_staff,name="edit_student_save_staff"),
    path('check_email_exist_staff',Staffview.check_email_exist_staff,name="check_email_exist_staff"),
    path('check_username_exist_staff', Staffview.check_username_exist_staff, name="check_username_exist_staff"),
    path('staff_add_result', Staffview.staff_add_result, name="staff_add_result"),
    path('save_student_result', Staffview.save_student_result, name="save_student_result"),



    path('student_home',Studentview.student_home,name="student_home"),
    path('student_view_attendance',Studentview.student_view_attendance,name="student_view_attendance"),
    path('student_view_attendance_post',Studentview.student_view_attendance_post,name="student_view_attendance_post"),
    path('student_view_result',Studentview.student_view_result,name="student_view_result"),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_URL)
