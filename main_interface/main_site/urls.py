"""med_analysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from main_interface.app import views
from django.contrib.auth.views import LoginView
from main_interface.app.forms import MyLoginForm



urlpatterns = [
    #path('', views.index_view, name='home'),
    path('analysis_list/', views.analysis_list, name='analysis_list'),
    path('analysis_list/<int:analysis_id>/', views.analysis_detail, name='analysis_detail'),
    path('charts/', views.charts, name='charts')
#    path('login/', views.login_view, name='login')
]