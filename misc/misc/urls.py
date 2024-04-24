"""
URL configuration for misc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from miscFunctions.trm import job as trm_job
from miscFunctions.inflation import job as inflation_job
from miscFunctions.person import job as person_job

urlpatterns = [
    path('admin/', admin.site.urls),
]

try:
    trm_job()
    inflation_job()
    person_job()
except:
    pass
