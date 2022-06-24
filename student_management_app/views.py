from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from student_management_app.EmailBackEnd import EmailBackEnd


# Create your views here.
def homepage(request):
    return render(request,'home.html')
def loginpage(request):
    return render(request,"login.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'),
                                         password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type=="1":
            #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
               return HttpResponseRedirect("/admin_home")
            elif user.user_type=="2":
                return HttpResponseRedirect("/staff_home")
            else:
                return HttpResponseRedirect("/student_home")
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")



def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: " + request.user.email + " User Type: " + request.user.user_type)
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
