"""
URL configuration for main_interface project.

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

from pages.views import home_view
from analysis.views import analysis_detail_view
from analysis.views import analysis_list_view
from login.views import login_view

urlpatterns = [
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
    path('admin/', admin.site.urls),
    # path('analysis_detail/', analysis_detail_view),
    path('analysis_list/', analysis_list_view, name='analysis_list'),
    path('analysis_list/<str:analysis_type>/', analysis_detail_view,
         name='analysis_detail'),
    path('login/', login_view, name='login_page')
]
