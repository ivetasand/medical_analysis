from django.shortcuts import render
from django.http import HttpResponse
from utils.database.interface import DbInterface


# Create your views here.
def login_view(request):
    return render(request, "login.html", {})
