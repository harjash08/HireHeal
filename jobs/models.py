from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
# Create your models here.

class Profile(models.Model):
    ROLE_CHOICES=[
        ('employee','Employee'),
        ('employer','Employer'),
    ]
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    role=models.CharField(max_length=10,choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username
    
class Employer(models.Model):
    SIZE_CHOICES=[
        ('1-10','1-10 Employees'),
        ('11-50','11-50 Employees'),
        ('51-200','51-200 Employees'),
        ('200+','200+ Employees'),
            
    ]
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    company_name=models.CharField(max_length=100)
    company_logo=models.ImageField(upload_to='company_logo/',blank=False,null=False)
    company_email=models.EmailField(max_length=254)
    phone=models.CharField(max_length=15)
    website=models.URLField(max_length=200,blank=False,null=False)
    company_description=models.TextField()
    location=models.CharField(max_length=100)
    industry=models.CharField(max_length=50)
    company_size=models.CharField(max_length=50,choices=SIZE_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name
    
class Jobs(models.Model):
    EXPERIENCE_CHOICES=[
        ('fresher','Freshers'),
        ('1-2','1-2 Years'),
        ('3-5','3-5 Years'),
        ('5+','5+ Years'),
            
    ]
    WORK_MODE_CHOICES=[
        ('onsite','onsite'),
        ('remote','remote'),
        ('hybrid','hybrid'),
    ]
    APPLICATION_METHOD_CHOICES=[
        ('platform','Apply on Platform'),
        ('external','External Link'),
    ]   
    STATUS_CHOICES=[
        ('Draft','Draft'),
        ('Published','Published'),
        ('Closed','Closed'),
        ('Active','Active')
    ] 
    
    employer=models.ForeignKey(User,related_name='posted_job',on_delete=models.CASCADE)
    company=models.ForeignKey(Employer,related_name='jobs', on_delete=models.CASCADE,null=True,blank=True)
    description=models.TextField()
    title=models.CharField(max_length=50,null=True,blank=True)
    experience_required=models.CharField(choices=EXPERIENCE_CHOICES ,max_length=50,null=True,blank=True)
    work_mode=models.CharField(choices=WORK_MODE_CHOICES,max_length=50,null=True,blank=True)
    salary_min=models.PositiveIntegerField(null=True,blank=True)
    salary_max=models.PositiveIntegerField(null=True,blank=True)
    responsibility=models.TextField(null=True,blank=True)
    skills=models.CharField(max_length=250,help_text="Enter skills seperated by commas",null=True,blank=True)
    application_deadline=models.DateField(default=timezone.now)
    application_method=models.CharField(max_length=20,choices=APPLICATION_METHOD_CHOICES,default='platform')
    application_email=models.EmailField(max_length=254,blank=True,null=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Draft')
    updated_at=models.DateTimeField(auto_now=True)
    location=models.CharField(max_length=100)
    job_type=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    

    def __str__(self):
        return self.title if self.title else "Untitled Job"


phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Enter a valid 10-digit phone number"
)
class Employee(models.Model):
     user=models.OneToOneField(User, on_delete=models.CASCADE)
     name=models.CharField(max_length=50,null=True)
     phone=models.CharField(max_length=10,validators=[phone_validator])
     location=models.CharField(max_length=100)
     profile_picture=models.ImageField(upload_to='profile_pics/', blank=False,null=False)
     skills=models.TextField()
     profesional_summary=models.TextField(blank=True)
     experience_years=models.IntegerField(default=0)
     resume=models.FileField(upload_to='resume/', blank=False,null=False)
     highest_qualification=models.CharField(max_length=100)
     college_name=models.CharField(max_length=50)
     graduation_year=models.IntegerField()

     def __str__(self):
         return self.user.username
     
class Application(models.Model):
    STATUS_CHOICES=[
        ('Pending','Pending'),
        ('Shortlisted','Shortlisted'),
        ('Interview_Scheduled','Interview_Scheduled'),
        ('Rejected','Rejected'),

    ]
    job=models.ForeignKey(Jobs,on_delete=models.CASCADE)
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=True)
    phone=models.CharField(max_length=15,null=True)
    email=models.EmailField(max_length=254,null=True)
    skills=models.TextField(null=True)
    resume=models.FileField(upload_to='resume/', max_length=100, blank=True,null=True)
    applied_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    def __str__(self):
        return f"{self.employee.user.username} applied for {self.job.title}"
    
class Savedjob(models.Model):
    job=models.ForeignKey(Jobs,on_delete=models.CASCADE)
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    saved_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.employee.name