from django.shortcuts import render,redirect
from jobs.forms import Registrationform
from jobs.models import Jobs
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.db.models import Q
from django.core.exceptions import SuspiciousOperation

def custom_404(request,exception):
    return render(request,'404.html',status=404)
def custom_500(request):
    return render(request,'500.html',status=500)
def custom_403(request,exception):
    return render(request,'403.html',status=403)
def custom_400(request,exception):
    return render(request,'400.html',status=400)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        form=Registrationform(request.POST)
        if form.is_valid():
            user=form.save()
            role=form.cleaned_data['role']
            profile=user.profile
            profile.role=role
            profile.save()
            return redirect('login_view')
        
    else:
        form=Registrationform()

    return render(request,'register.html',{'form':form})
def home(request):
        keyword=request.GET.get('search')
        total_jobs=Jobs.objects.all()
        if request.GET.get('search'):
         total_jobs=Jobs.objects.filter(Q(title__icontains=keyword) | Q(company__company_name__icontains=keyword) | Q(location__icontains=keyword) | Q(created_at__icontains=keyword))
    
   
        context={
        'total_jobs':total_jobs,
        'keyword':keyword
        }
        return render(request,'employees.html',context)


def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(request,request.POST)   
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('home')

    else:
         form=AuthenticationForm()
    return render(request,'login.html',{'form':form})



def logout_view(request):
    logout(request)
    return redirect('login_view')

