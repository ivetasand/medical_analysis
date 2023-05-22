from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html")


# def login_view(*args, **kwargs):
#     return HttpResponse("<h1>Login view</h1>")
#
#
# def analysis_view(*args, **kwargs):
#     return HttpResponse("<h1>Analysis view</h1>")
