from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Register your models here.
from student_management_app.models import CustomUser


class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)
