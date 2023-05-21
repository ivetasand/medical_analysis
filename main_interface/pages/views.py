from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    my_context = {
        "my_text": "This is about us",
        "my_number": 123,
        "my_list": [123, "ads", 312],
        "this_is_True": 312
    }
    return render(request, "home.html", my_context)


def login_view(*args, **kwargs):
    return HttpResponse("<h1>Login view</h1>")


def analysis_view(*args, **kwargs):

    return HttpResponse("<h1>Analysis view</h1>")
