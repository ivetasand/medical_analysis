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
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic import RedirectView

from pages.views import home_view
from analysis.views import analysis_detail_view, analysis_list_view, \
    analysis_numeric_edit_view, choice_view, analysis_text_edit_view
from login.views import login_view, login_data_post_view
from well_being.views import well_being_list_view, well_being_detail_view, \
    steps_edit_view

urlpatterns = [
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('analysis_list/', analysis_list_view, name='analysis_list'),
    path('analysis_list/<str:analysis_type>/', analysis_detail_view,
         name='analysis_detail'),
    path('login/', login_view, name='login_page'),
    path('well_being/', well_being_list_view, name='well_being_list'),
    path('well_being/<str:well_being_type>/', well_being_detail_view,
         name='well_being_detail'),
    path("favicon.ico",
         RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),
    path('login_data_post/', login_data_post_view, name='login_data_post'),
    path('analysis_edit/', choice_view, name='analysis_edit_choice'),
    path('analysis_edit/numeric/', analysis_numeric_edit_view,
         name='analysis_edit_numeric'),
    path('analysis_edit/text/', analysis_text_edit_view,
         name='analysis_edit_text'),
    path('analysis_edit/steps/', steps_edit_view,
         name='steps_edit')
]
