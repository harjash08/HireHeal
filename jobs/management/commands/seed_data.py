from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Profile, Employer, Employee, Jobs, Application
from faker import Faker
import random

# Dummy data for testing
fake = Faker()

class Command(BaseCommand):
    help = 'Seed full data according to models'

    def handle(self, *args, **kwargs):

        employers = []
        employees = []
        jobs = []

        # -------------------------
        # CREATE EMPLOYERS
        # -------------------------
        for i in range(3):
            username = fake.user_name()

            if User.objects.filter(username=username).exists():
                continue

            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password='1234'
            )

            Profile.objects.get_or_create(user=user, defaults={'role': 'employer'})

            employer = Employer.objects.create(
                user=user,
                company_name=fake.company(),
                company_logo='company_logo/user.jpeg',
                company_email=fake.email(),
                phone='9876543210',
                website=fake.url(),
                company_description=fake.text(),
                location=fake.city(),
                industry="IT",
                company_size=random.choice(['1-10', '11-50', '51-200', '200+'])
            )

            employers.append(employer)

        # -------------------------
        # CREATE EMPLOYEES
        # -------------------------
        for i in range(5):
            username = fake.user_name()

            if User.objects.filter(username=username).exists():
                continue

            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password='1234'
            )

            Profile.objects.get_or_create(user=user, defaults={'role': 'employee'})

            employee = Employee.objects.create(
                user=user,
                name=fake.name(),
                phone='9876543210',
                location=fake.city(),
                profile_picture='profile_pics/user.jpeg',
                skills=", ".join(fake.words(nb=5)),
                profesional_summary=fake.text(),
                experience_years=random.randint(0, 5),
                resume='resume/file.pdf',
                highest_qualification="B.Tech",
                college_name=fake.company(),
                graduation_year=random.randint(2018, 2024)
            )

            employees.append(employee)

        # -------------------------
        # INCLUDE EXISTING DATA
        # -------------------------
        employers += list(Employer.objects.all())
        employees += list(Employee.objects.all())

        # -------------------------
        # CREATE JOBS
        # -------------------------
        for emp in employers:
            for i in range(2):
                job = Jobs.objects.create(
                    employer=emp.user,  # IMPORTANT ✅
                    company=emp,
                    title=random.choice([
                        "Frontend Developer",
                        "Backend Developer",
                        "Full Stack Developer",
                        "UI/UX Designer"
                    ]),
                    description=fake.text(),
                    experience_required=random.choice(['fresher', '1-2', '3-5']),
                    work_mode=random.choice(['onsite', 'remote', 'hybrid']),
                    salary_min=20000,
                    salary_max=80000,
                    responsibility=fake.text(),
                    skills=", ".join(fake.words(nb=5)),
                    application_email=fake.email(),
                    status='Active',
                    location=fake.city(),
                    job_type="Full-time"
                )
                jobs.append(job)

        jobs += list(Jobs.objects.all())

        # -------------------------
        # CREATE APPLICATIONS
        # -------------------------
        for emp in employees:
            random_jobs = random.sample(jobs, min(3, len(jobs)))

            for job in random_jobs:
                if not Application.objects.filter(employee=emp, job=job).exists():
                    Application.objects.create(
                        job=job,
                        employee=emp,
                        name=emp.name,
                        phone=emp.phone,
                        email=emp.user.email,
                        skills=emp.skills,
                        resume='resume/my_cv.docx',
                        status=random.choice(['Pending', 'Shortlisted', 'Rejected'])
                    )

        self.stdout.write(self.style.SUCCESS("✅ Data seeded successfully!"))