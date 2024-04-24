from django.urls import path
from . import views

urlpatterns = [
    path('persons', views.persons, name='persons'),
    path('trms', views.trms, name='trm')
]