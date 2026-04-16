from .models import Jobs,Application,Employee
def get_jobs(request):
    fil_jobs_count=0
    fil_jobs_active=None
    fil_jobs_closed=None
    total_jobs=[]
    total_employee=[]
    fil_appli_active=None
    if request.user.is_authenticated:
        fil_jobs=Jobs.objects.filter(employer=request.user)
        fil_jobs_count=Jobs.objects.filter(employer=request.user).count()
        fil_appli_active=Application.objects.filter(job__employer=request.user).count()
        fil_jobs_active=Jobs.objects.filter(employer=request.user,status='Active').count()
        fil_jobs_closed=Jobs.objects.filter(employer=request.user,status='Closed').count()
        total_jobs=Jobs.objects.all()
        total_employee=Employee.objects.all()
        
    else:
        fil_jobs=Jobs.objects.none()
    return dict(fil_jobs=fil_jobs,fil_jobs_count=fil_jobs_count,fil_jobs_active=fil_jobs_active,fil_jobs_closed=fil_jobs_closed,total_jobs=total_jobs,fil_appli_active=fil_appli_active,total_employee=total_employee)