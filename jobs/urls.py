from django.urls import path
from . import views


urlpatterns = [
   
    path('', views.dashboard, name='dashboard'),
    path('company_profile/', views.company_profile, name='company_profile'),
    path('edit_company_profile/', views.edit_company_profile, name='edit_company_profile'),
    path('post_jobs/', views.post_jobs, name='post_jobs'),
    path('manage_job/', views.manage_job, name='manage_job'),
    path('manage_job/edit/<int:edit_id>', views.edit, name='edit'),
    path('manage_job/delete/<int:delete_id>', views.delete, name='delete'),
    path('manage_job/view_job/<int:view_id>', views.view_job, name='view_job'),
    path('application/<int:job_id>', views.application, name='application'),
    path('finalize/', views.finalize, name='finalize'),
    path('employer_application/', views.employer_application, name='employer_application'),
    path('employer_application/update_application_status/<int:app_id>/<str:status>/', views.update_application_status, name='update_application_status'),
    path('savejob/<int:job_id>', views.savejob, name='savejob'),
    path('saved_jobs/', views.saved_jobs, name='saved_jobs'),
    path('removesavedjob/<int:saved_id>', views.removesavedjob, name='removesavedjob'),
    path('schedule_interview/<int:app_id>', views.schedule_interview, name='schedule_interview'),

    
]

