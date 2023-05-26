import json

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from main_backend.main_service import Service
from utils.database.interface import DbInterface


@csrf_exempt
def login_view(request):
    if request.method == 'POST' and 'get_analysis_button' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        laboratory = request.POST['lab_id']

        if username == "" or password == "":
            messages.error(request, 'Введены неверные данные пользователя')
            return HttpResponseRedirect('http://127.0.0.1:7000/login/')

        service = Service()
        db = DbInterface()
        result = service.get_med_service(laboratory, username, password)

        if result == 'Error 1':
            messages.error(request, 'Введены неверные данные пользователя')
            return HttpResponseRedirect('http://127.0.0.1:7000/login/')
        elif result == 'Error 2':
            messages.error(request, 'Нет доступных анализов')
            return HttpResponseRedirect('http://127.0.0.1:7000/login/')

        messages.error(request, f'Всего анализов обработано {len(result) - 1}. '
                                f'Анализов не считано {result[-1]}')
        db.insert_analysis_data(result[:-1])
        return HttpResponseRedirect('http://127.0.0.1:7000/login/')

    elif request.method == 'POST' and 'get_steps_data' in request.POST:
        return HttpResponseRedirect('http://127.0.0.1:7000/login/')
    else:
        return render(request, 'login.html', {})

@csrf_exempt
def login_data_post_view(request):
    if request.method == 'POST' and not ('get_steps_data' in request.POST or
                                         'get_analysis_button' in request.POST):
        subject = request.body
        subject_data = json.loads(subject)

        db = DbInterface()
        result = []

        for key, value in subject_data.items():
            result.append(value)

        count = db.insert_steps_data(result)
        messages.error(request, f'Всего дней с данными шагов обработано {count}.')

    return HttpResponseRedirect('http://127.0.0.1:7000/login/')
