from django.contrib import admin
from .models import Market_User,CustomUser
# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title','name','created','code','linenos')



class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name','mobile_number','email','gender','age_group','subscription','price','image')

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','username','password','email','first_name','last_name','mobile_number','address','user_type')
# admin.site.register(User)
admin.site.register(Market_User)
admin.site.register(CustomUser)
  
