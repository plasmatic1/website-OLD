from django.urls import path

from view_utils import not_implemented
from .views import *

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('resume/', resume, name='resume'),
    path('projs/', not_implemented, name='projects_and_contests')
]
