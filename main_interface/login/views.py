from django.contrib import messages
from django.shortcuts import render


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        laboratory = request.POST['lab_id']

        print(laboratory, username, password)

        if username == "" or password == "":
            messages.error(request, 'Введены неверные данные пользователя')
            return render(request, 'login.html')

        # тут будем доставать инфу с сайта

    else:
        return render(request, 'login.html')
