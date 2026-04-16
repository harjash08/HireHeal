from django.contrib import admin
from .models import Profile,Employer,Jobs,Employee,Application,Savedjob
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class Profileadmin(admin.ModelAdmin):
    list_display=('user','role')
class Employeradmin(admin.ModelAdmin):
    list_display=('user','company_name','company_email','website','industry')
    search_fields=('company_name','website','industry')
class Jobsadmin(admin.ModelAdmin):
    list_display=('employer','location','job_type','is_active')
 
class CustomAdminSite(admin.AdminSite):
    def has_permission(self, request):
        return request.user.is_authenticated and request.user.is_superuser

admin_site = CustomAdminSite(name='custom_admin')
   
admin_site.register(Profile,Profileadmin) 
admin_site.register(Employer,Employeradmin)
admin_site.register(Jobs,Jobsadmin)
admin_site.register(Employee)
admin_site.register(Application)
admin_site.register(Savedjob)
admin_site.register(User, UserAdmin)



