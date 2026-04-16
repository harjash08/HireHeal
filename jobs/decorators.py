from django.shortcuts import render

def employer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.role == 'employer':
                return view_func(request, *args, **kwargs)
        return render(request,'403.html',status=403)
    return wrapper


def employee_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.role == 'employee':
                return view_func(request, *args, **kwargs)
        return render(request,'403.html',status=403)
    return wrapper