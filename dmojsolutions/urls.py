from django.urls import path

from dmojsolutions.views.index import index

app_name = 'dmojsolutions'

urlpatterns = [
    path('', index, name='index')
]
