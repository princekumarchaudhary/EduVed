from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse ,JsonResponse
from student_management_app.models import Subjects,Students,Attendance,AttendanceReport,Courses,CustomUser,Staffs,StudentResult

def staff_home(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    course_id_list=[]
    for subject in subjects:
        course=Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course)
    final_course=[]
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)
    students_count=Students.objects.filter(course_id__in=final_course).count()

    attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()
    subject_count=subjects.count()

    return render(request,"staff_template/staff_home_template.html",{"students_count":students_count,"attendance_count":attendance_count,"subject_count":subject_count})
def staff_taken_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    return render(request,"staff_template/staff_taken_attendance.html",{"subjects":subjects})

@csrf_exempt
def get_students(request):
    subject_id = request.POST.get("subject")
    subject_model = Subjects.objects.get(id=subject_id)
    students = Students.objects.filter(course_id=subject_model.course_id)
    list_data = []

    for student in students:
        data_small = {"id": student.admin.id, "name": student.admin.first_name + " " + student.admin.last_name}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    subject_model=Subjects.objects.get(id=subject_id)
    json_sstudent=json.loads(student_ids)
    try:
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date)
        attendance.save()

        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERROR")

def staff_update_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    return render(request,"staff_template/staff_update_attendance.html",{"subjects":subjects})

@csrf_exempt
def get_attendance_dates(request):
    subject_id = request.POST.get("subject")
    subject_model = Subjects.objects.get(id=subject_id)
    attendance = Attendance.objects.filter(subject_id=subject_model)
    list_data = []

    for attendance_single in attendance:
        data_small = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date)}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def get_attendance_student(request):
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def update_attendance_data(request):
    student_ids = request.POST.get("student_ids")

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_student = json.loads(student_ids)

    try:

        for stud in json_student:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status = stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")

def add_student_staff(request):
    courses=Courses.objects.all()
    return render(request,"staff_template/add_student_staff.html",{'courses':courses})

def add_student_save_staff(request):
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
            return HttpResponseRedirect("/add_student_staff")
          except:
            messages.error(request, "Failed to Add Sudent")
            return HttpResponseRedirect("/add_student_staff")

def manage_student_staff(request):
    students=Students.objects.all()
    return render(request,"staff_template/manage_student_staff.html",{"students":students})

def edit_student_staff(request,student_id):
    courses=Courses.objects.all
    student=Students.objects.get(admin=student_id)
    return render(request,"staff_template/edit_student_staff.html",{"student":student,"courses":courses,"id":student_id})

def edit_student_save_staff(request):
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
            return HttpResponseRedirect("/edit_student_staff/" + student_id)
        except:
            messages.error(request, "Failed to Edit Student")
            return HttpResponseRedirect("/edit_student_staff/" + student_id)

@csrf_exempt
def check_email_exist_staff(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist_staff(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def staff_add_result(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    return render(request, "staff_template/staff_add_result.html",{"subjects":subjects})
def save_student_result(request):
        if request.method != "POST":
            messages.error(request, "Invalid Method")
            return redirect('staff_add_result')
        else:
            student_admin_id = request.POST.get('student_list')
            assignment_marks = request.POST.get('assignment_marks')
            exam_marks = request.POST.get('exam_marks')
            subject_id = request.POST.get('subject')

            student_obj = Students.objects.get(admin=student_admin_id)
            subject_obj = Subjects.objects.get(id=subject_id)

            try:
                check_exist = StudentResult.objects.filter(subject_id=subject_obj, student_id=student_obj).exists()
                if check_exist:
                    result = StudentResult.objects.get(subject_id=subject_obj, student_id=student_obj)
                    result.subject_assignment_marks = assignment_marks
                    result.subject_exam_marks = exam_marks
                    result.save()
                    messages.success(request, "Result Updated Successfully!")
                    return redirect('staff_add_result')
                else:
                    result = StudentResult(student_id=student_obj, subject_id=subject_obj,
                                           subject_exam_marks=exam_marks, subject_assignment_marks=assignment_marks)
                    result.save()
                    messages.success(request, "Result Added Successfully!")
                    return redirect('staff_add_result')
            except:
                messages.error(request, "Failed to Add Result!")
                return redirect('staff_add_result')



