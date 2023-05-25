import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from main_backend.main_service import Service
from utils.database.interface import DbInterface


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        laboratory = request.POST['lab_id']

        if username == "" or password == "":
            messages.error(request, 'Введены неверные данные пользователя')
            return render(request, 'login.html')

        service = Service()
        db = DbInterface()
        print(service.get_med_service(laboratory, username, password))
        # db.insert_analysis_data(service.get_med_service(laboratory, username, password)[:-1])

        # тут будем доставать инфу с сайта
        # здесь будет инфа про сайт
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def login_data_post_view(request):
    if request.method == 'POST':
        subject = request.body
        subject_data = json.loads(subject)
        return JsonResponse(subject_data, status=200)
    return JsonResponse(status=400)
