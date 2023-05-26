import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from main_backend.main_service import Service
from utils.database.interface import DbInterface
from django.urls import reverse


@csrf_exempt
def login_view(request):
    if request.method == 'POST' and 'get_analysis_button' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        laboratory = request.POST['lab_id']

        if username == "" or password == "":
            messages.error(request, 'Введены неверные данные пользователя')
            return redirect('login.html')

        service = Service()
        db = DbInterface()
        print(service.get_med_service(laboratory, username, password))
        # db.insert_analysis_data(service.get_med_service(laboratory, username, password)[:-1])

        # тут будем доставать инфу с сайта
        # здесь будет инфа про сайт
    elif request.method == 'POST' and 'get_steps_data' in request.POST:
        service = Service()
        print(service.get_med_service('google_fit'))
    else:
        return render(request, 'login.html', {})

@csrf_exempt
def login_data_post_view(request):
    if request.method == 'POST' and not ('get_steps_data' in request.POST or
                                         'get_analysis_button' in request.POST):
        subject = request.body
        subject_data = json.loads(subject)
        print(f'yo result {subject_data}')

    return redirect('login.html')
