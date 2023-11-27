"""
URL configuration for HumanResources project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/', views.read_all_employees, name='read_all_employees'),
    path('employee/<int:employee_id>', views.read_one_record),
    path('employee/update', views.update_employee),
    path('employee/<int:employee_id>/delete', views.delete_employee),
    path('employee/insert', views.insert_record_into_table),
    path('employees/get_average_age_per_industry', views.get_average_age_per_industry),
    path('employees/get_average_salary_per_industry', views.get_average_salary_per_industry),
    path('employees/get_average_salary_per_years_of_experience',
          views.get_average_salary_per_years_of_exp),
    path('employees/get_other_interesting_stats', views.get_other_interesting_stats)
]
