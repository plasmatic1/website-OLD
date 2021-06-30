"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

from view_auth import logout_user, LoginFormView, login_as_guest

urlpatterns = [
    # Path to subpages
    path('dmojsols/admin/', admin.site.urls, name='admin'),
    path('dmojsols/', include('dmojsolutions.urls', namespace='dmojsolutions')),
    # path('todo/', include('todolist.urls', namespace='todolist')),

    # Logging in/out
    path('dmojsols/login/', LoginFormView.as_view(), name='login'),
    path('dmojsols/logout/', logout_user, name='logout'),

    # Other utility things
    path('dmojsols/login_as_guest/', login_as_guest, name='login_as_guest'),
]
