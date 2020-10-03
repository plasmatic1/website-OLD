from django.urls import path

from view_utils import not_implemented

app_name = 'blog'

urlpatterns = [
    path('', not_implemented, name='index')
]
