from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Jobs,Employee,Application,Employer
from django import forms

class Registrationform(UserCreationForm):
    role=forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)
    class Meta:
        model=User
        fields=('email','username','password1','password2','role')

class Postjobform(forms.ModelForm):
    class Meta:
        model=Jobs
        fields=('description','title','experience_required','work_mode','salary_min','salary_max','responsibility','skills','application_deadline','application_method','application_email','status','location','job_type')

class Profileform(forms.ModelForm):
    class Meta:
        model=Employee
        fields=('name','phone','location','profile_picture','skills','profesional_summary','experience_years','resume','highest_qualification','college_name','graduation_year')
        

class Applicationform(forms.ModelForm):
    class Meta:
        model=Application
        fields=('name','phone','email','skills','resume')



class InterviewEmailForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, required=True)

class Company_profile(forms.ModelForm):
    class Meta:
        model=Employer
        fields=('company_name','company_logo','company_email','phone','website','company_description','location','industry','company_size')