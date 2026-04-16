from .models import Jobs, Application, Employee


def get_jobs(request):
    user = getattr(request, "user", None)

    fil_jobs = Jobs.objects.none()
    fil_jobs_count = 0
    fil_jobs_active = 0
    fil_jobs_closed = 0
    fil_appli_active = 0

    total_jobs = Jobs.objects.all()
    total_employee = Employee.objects.all()

    if user and getattr(user, "is_authenticated", False):

        fil_jobs = Jobs.objects.filter(employer=user)
        fil_jobs_count = fil_jobs.count()

        fil_appli_active = Application.objects.filter(job__employer=user).count()

        fil_jobs_active = Jobs.objects.filter(
            employer=user, status='Active'
        ).count()

        fil_jobs_closed = Jobs.objects.filter(
            employer=user, status='Closed'
        ).count()

    return {
        'fil_jobs': fil_jobs,
        'fil_jobs_count': fil_jobs_count,
        'fil_jobs_active': fil_jobs_active,
        'fil_jobs_closed': fil_jobs_closed,
        'fil_appli_active': fil_appli_active,
        'total_jobs': total_jobs,
        'total_employee': total_employee,
    }