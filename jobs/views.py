from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Employer,Jobs,Employee,Application,Savedjob,Profile
from .forms import Postjobform,Profileform,Applicationform,InterviewEmailForm,Company_profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .decorators import employer_required
from .decorators import employee_required
def company_profile(request):
    
        Company=Employer.objects.filter(user=request.user).first()
        if not Company:
            return redirect('edit_company_profile')
        jobs=Jobs.objects.filter(employer=request.user)
        context={
        'company':Company,
        'jobs':jobs
        }
        return render(request,'dashboard/company_profile.html',context)
    
    
def edit_company_profile(request):
         try:
            profile=Employer.objects.get(user=request.user)
         except Employer.DoesNotExist:
            profile=None
         if request.method=='POST':
            form=Company_profile(request.POST,request.FILES,instance=profile)
            if form.is_valid():
                profile=form.save(commit=False)
                profile.user=request.user
                profile.save()
            return redirect('company_profile')
         else:
            form=Company_profile(instance=profile)
         context={
            'profile':profile,
            'form':form
                }
         return render(request,'dashboard/edit_company_profile.html',context)


@login_required(login_url='login_view')
def dashboard(request):
    jobs=Jobs.objects.all()
    job_count=Jobs.objects.filter(employer=request.user).count()
    job_active=Jobs.objects.filter(is_active=True,employer=request.user).count()
    allemployee=Employee.objects.all()
    print(allemployee)
    context={
        'job_count':job_count,
        'job_active':job_active,
        'jobs':jobs
    }
    return render(request,'dashboard/home.html',context)
@employer_required
def post_jobs(request):
    employer = Employer.objects.filter(user=request.user).first()
    if not employer:
        return redirect("edit_company_profile")
    if request.method=='POST':
        form=Postjobform(request.POST)
        if form.is_valid():
            job=form.save(commit=False)
            job.employer=request.user
            job.company=employer
            job.save()
            return redirect('company_profile')
    else:
        form=Postjobform()

    return render(request,'dashboard/post_jobs.html',{'form':form})

def manage_job(request):
    
    return render(request,'dashboard/manage.html')

def edit(request,edit_id):
     job=get_object_or_404(Jobs,pk=edit_id)
     if request.method=='POST':
        form=Postjobform(request.POST,instance=job)
        if form.is_valid():
            form.save()
            return redirect('manage_job')
     else:
        form=Postjobform(instance=job)
     context={
        'form':form,
        'job':job
    }
    
     return render(request,'dashboard/edit.html',context)

def delete(request,delete_id):
     job=get_object_or_404(Jobs,pk=delete_id)
     job.delete()
     return redirect('manage_job')

def view_job(request,view_id):
    job=get_object_or_404(Jobs,pk=view_id)
    return render(request,'dashboard/view.html',{'job':job})

def edit_profile(request):
    try:
        profile=Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        profile=None
    
    if request.method=='POST':
        form=Profileform(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect('profile')
    else:
        form=Profileform(instance=profile)
    context={
        'profile':profile,
        'form':form
    }
    return render(request,'edit_profile.html',context)



def profile(request, id=None):

    # employee viewing own profile
    if id is None:
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return redirect('edit_profile')

    # employer viewing employee profile
    else:
        employee = Employee.objects.get(id=id)

    if employee.skills:
        skills_list = [skill.strip() for skill in employee.skills.split(",")]
    else:
        skills_list = []

    return render(request,'profile.html',{
        'employee':employee,
        'skills_list':skills_list
    })

def viewjob(request,view_id):
    job=get_object_or_404(Jobs,pk=view_id)
    if job.skills:
        skills_required=[skill.strip()for skill in job.skills.split(",")]
    else:
        skills_required=[]
    return render (request,'viewjob.html',{'job':job,'skills_required':skills_required})
@employee_required
def application(request,job_id):
    
        job= get_object_or_404(Jobs, pk=job_id)
        employee = Employee.objects.filter(user=request.user).first()
        if not employee:
            return redirect('profile')
        if request.method=='POST':
            form=Applicationform(request.POST,request.FILES)
            if form.is_valid():
                application=form.save(commit=False)
                application.job=job
                application.employee=employee
                application.save()
                messages.success(request,"Application submited successfully")
                return redirect('finalize')
        else:
            form=Applicationform()
   

        return render(request,'application.html',{'form':form})


def finalize(request):
    employee=Employee.objects.filter(user=request.user).first()
    if not employee:
        return redirect('profile')
    totalappli = Application.objects.filter(employee=employee).select_related('job').order_by('applied_at')
    
    return render(request, 'finalize.html', {'totalappli': totalappli})

def employer_application(request):
    applications=Application.objects.filter(job__employer=request.user).select_related('job','employee')
    return render(request, 'dashboard/application.html', {'applications': applications})

def update_application_status(request,app_id,status):
    application=Application.objects.get(id=app_id)
    if application.job.employer!=request.user:
        return redirect('dashboard')
    if status == "Interview_Scheduled":
        return redirect('schedule_interview',app_id=application.id)
    application.status=status
    application.save()
    return redirect('employer_application')



def saved_jobs(request):
    employee =Employee.objects.filter(user=request.user).first()
    if not employee:
            return redirect('profile')
    allsavedjobs=Savedjob.objects.filter(employee=employee)
    return render(request, 'savedjob.html', {
        'allsavedjobs': allsavedjobs
    })
def savejob(request, job_id):
    job = get_object_or_404(Jobs, pk=job_id)
    employee = Employee.objects.filter(user=request.user).first()
    if not employee:
            return redirect('profile')
    # Save job (no duplicates)
    saved_job, created = Savedjob.objects.get_or_create(
        job=job,
        employee=employee
    )

    # Get all saved jobs for display
    allsavedjobs = Savedjob.objects.filter(employee=employee)

    return redirect('saved_jobs')



def removesavedjob(request,saved_id):
    deletejob=get_object_or_404(Savedjob,pk=saved_id)
    
    deletejob.delete()
    return redirect('saved_jobs')



def schedule_interview(request, app_id):
    application = Application.objects.get(id=app_id)

    if request.method == "POST":
        form = InterviewEmailForm(request.POST)
        if form.is_valid():
            custom_message = form.cleaned_data['message']

            # update status
            application.status = "Interview Scheduled"
            application.save()

            # send email
            send_mail(
                subject="Interview Scheduled",
                message=f"""
Hello {application.name}, You have been selected for the interview

{custom_message}

Job: {application.job.title}

Best of luck!
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[application.email],
                fail_silently=False,
            )

            return redirect('employer_application')

    else:
        form = InterviewEmailForm()

    return render(request, 'schedule_interview.html', {'form': form})