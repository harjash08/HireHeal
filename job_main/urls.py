"""
URL configuration for job_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from jobs.admin import admin_site
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from jobs import views as jobviews

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', views.register, name='register'),
    path('home/', views.home, name='home'),
     path('login_view/', views.login_view, name='login_view'),
     path('logout_view/', views.logout_view, name='logout_view'),
     path('profile/', jobviews.profile, name='profile'),
      path('profile/<int:id>/',jobviews.profile, name='profile'),
      path('viewjob/<int:view_id>', jobviews.viewjob, name='viewjob'),
     path('edit_profile/', jobviews.edit_profile, name='edit_profile'),
     path('dashboard/', include('jobs.urls')),
]
handler404='job_main.views.custom_404'
handler500='job_main.views.custom_500'
handler403='job_main.views.custom_403'
handler400='job_main.views.custom_400'
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)