from django.shortcuts import render
from django.http import HttpResponse
from utils.database.interface import DbInterface
import json


# Create your views here.
def well_being_list_view(request):
    #  for testing
    #  interface = DbInterface()
    return render(request, "well_being/list.html", {'well_being_list': ["Шаги"]})


def well_being_detail_view(request, well_being_type):
    # тут надо добавить варианты, что если тип такой, то грузим такой html
    # тут собираем данные из бд и кладем в контекст
    # data = [['2023-04-11', 1234], ['2023-04-12', 432]]
    interface = DbInterface()
    data = interface.fetch_steps_data()

    dates = [sublist[0] for sublist in data]
    steps = [sublist[1] for sublist in data]

    context = {
        'dates': dates,
        'steps': steps
    }
    return render(request, "well_being/detail.html", context)
