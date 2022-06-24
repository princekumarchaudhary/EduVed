from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from student_management_app.models import CustomUser,Courses,Subjects,Staffs,Students,Attendance,AttendanceReport

def admin_home(request):
    student_count=Students.objects.all().count()
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.all().count()
    course_count=Courses.objects.all().count()
    context={
        "student_count":student_count,
        "staff_count":staff_count,
        "subject_count":subject_count,
        "course_count":course_count
    }
    return render(request,"hod_template/home_template.html",context)

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
     if request.method!="POST":
         return HttpResponse("Method Not Allowed")

     else:
       first_name=request.POST.get("first_name")
       last_name = request.POST.get("last_name")
       username = request.POST.get("username")
       email = request.POST.get("email")
       password = request.POST.get("password")
       address = request.POST.get("address")
       try:
         user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
         user.staffs.address=address
         user.save()
         messages.success(request,"Successfully Added Staff")
         return HttpResponseRedirect("/add_staff")
       except:
           messages.error(request, "Failed to Add Staff")
           return HttpResponseRedirect("/add_staff")

def add_course(request):
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        course=request.POST.get("course")
        try:
           course_model=Courses(course_name=course)
           course_model.save()
           messages.success(request, "Successfully Added Course")
           return HttpResponseRedirect("/add_course")
        except:
            messages.error(request, "Failed To Add Course")
            return HttpResponseRedirect("/add_course")

def add_student(request):
    courses=Courses.objects.all()
    return render(request,"hod_template/add_student_template.html",{'courses':courses})

def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")

    else:

          first_name = request.POST.get("first_name")
          last_name = request.POST.get("last_name")
          username = request.POST.get("username")
          email = request.POST.get("email")
          password = request.POST.get("password")
          address = request.POST.get("address")
          course_id=request.POST.get("course")
          sex=request.POST.get("sex")
          if len(request.FILES) != 0:
             profile_pic=request.FILES['profile_pic']
             fs=FileSystemStorage()
             filename=fs.save(profile_pic.name,profile_pic)
             profile_pic_url=fs.url(filename)
          else:
              profile_pic_url = None



          try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  last_name=last_name, first_name=first_name, user_type=3)
            user.students.address = address
            course_obj=Courses.objects.get(id=course_id)
            user.students.course_id=course_obj
            user.students.gender=sex
            user.students.profile_pic=profile_pic_url
            user.save()
            messages.success(request, "Successfully Added Student")
            return HttpResponseRedirect("/add_student")
          except:
            messages.error(request, "Failed to Add Sudent")
            return HttpResponseRedirect("/add_student")


def add_subject(request):
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html",{"staffs":staffs,"courses":courses})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)
        try:
            subject=Subjects(subject_name=subject_name,course_id=course,staff_id=staff)
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect("/add_subject")
        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect("/add_subject")


def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs})

def manage_student(request):
    students=Students.objects.all()
    return render(request,"hod_template/manage_student_template.html",{"students":students})

def manage_course(request):
    courses=Courses.objects.all()
    return render(request,"hod_template/manage_course_template.html",{"courses":courses})

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects})


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)

    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "hod_template/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Staff Updated Successfully.")
            return redirect('/edit_staff/' + staff_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_staff/' + staff_id)


def edit_student(request,student_id):
    courses=Courses.objects.all
    student=Students.objects.get(admin=student_id)
    return render(request,"hod_template/edit_student_template.html",{"student":student,"courses":courses,"id":student_id})
    pass

def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        address = request.POST.get("address")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")

        if request.FILES.get('profile_pic',False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            student=Students.objects.get(admin=student_id)
            student.address=address
            student.gender=sex
            courses=Courses.objects.get(id=course_id)
            student.course_id=courses
            if profile_pic_url!=None:
              student.profile_pic=profile_pic_url
            student.save()

            messages.success(request, "Student is Successfully Edited")
            return HttpResponseRedirect("/edit_student/" + student_id)
        except:
            messages.error(request, "Failed to Edit Student")
            return HttpResponseRedirect("/edit_student/" + student_id)


def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"courses":courses,"id":subject_id})
def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        course_id=request.POST.get("course")

        try:
           subject=Subjects.objects.get(id=subject_id)
           subject.subject_name=subject_name
           staff=CustomUser.objects.get(id=staff_id)
           subject.staff_id=staff
           course=Courses.objects.get(id=course_id)
           subject.course_id=course
           subject.save()
           messages.success(request, "Subject is Successfully Edited")
           return HttpResponseRedirect("/edit_subject/" + subject_id)
        except:
            messages.error(request, "Failed to Edit Subject")
            return HttpResponseRedirect("/edit_subject/" + subject_id)

def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course,"id":course_id})
def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")

        try:
           course=Courses.objects.get(id=course_id)
           course.course_name=course_name
           course.save()
           messages.success(request, "Course is Successfully Edited")
           return HttpResponseRedirect("/edit_course/" + course_id)
        except:
            messages.error(request, "Failed to Edit Course")
            return HttpResponseRedirect("/edit_course/" + course_id)






@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, "hod_template/admin_view_attendance.html", context)

@csrf_exempt
def admin_get_attendance_dates(request):
    subject_id = request.POST.get("subject")
    subject_model = Subjects.objects.get(id=subject_id)
    attendance = Attendance.objects.filter(subject_id=subject_model)
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date)}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

