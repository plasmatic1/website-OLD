from django.urls import path

from todolist.views import index, problems, homework, projects, remove_problem, remove_subject, remove_homework
from view_utils import not_implemented

app_name = 'todolist'

urlpatterns = [
    path('', index, name='index'),

    path('problems', problems, name='problems'),
    path('problems/rem/<int:problem_id>', remove_problem, name='remove_problem'),

    path('homework', homework, name='homework'),
    path('homework/rem/sub/<int:subject_id>', remove_subject, name='remove_subject'),
    path('homework/rem/hw/<int:homework_id>', remove_homework, name='remove_homework'),

    path('projects', projects, name='projects'),
    path('projects/rem/<int:project_id>', not_implemented, name='remove_project')
]
