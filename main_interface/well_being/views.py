from django.shortcuts import render
from django.http import HttpResponse
from utils.database.interface import DbInterface
import json


# Create your views here.
def well_being_list_view(request):
    #  for testing
    #  interface = DbInterface()
    return render(request, "well_being/list.html", {'well_being_list': ""})


def well_being_detail_view(request, well_being_type):
    # тут надо добавить варианты, что если тип такой, то грузим такой html
    # тут собираем данные из бд и кладем в контекст
    return render(request, "well_being/detail.html", {'well_being_list': ""})
