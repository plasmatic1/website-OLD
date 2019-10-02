from django.urls import path

from dmojsolutions.views.admin import reload_problems, reload_solutions, delete_problems, delete_solutions
from dmojsolutions.views.index import index, view, raw

app_name = 'dmojsolutions'

urlpatterns = [
    path('', index, name='index'),
    path('view/<str:code>/<str:lang>', view, name='view'),
    path('raw/<str:code>/<str:lang>', raw, name='raw'),

    # Admin Stuff
    path('reload_problems', reload_problems, name='reload_problems'),
    path('reload_solutions', reload_solutions, name='reload_solutions'),
    path('delete_problems', delete_problems, name='delete_problems'),
    path('delete_solutions', delete_solutions, name='delete_solutions')
]
