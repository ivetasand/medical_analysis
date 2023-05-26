from django.shortcuts import render
from utils.database.interface import DbInterface


def well_being_list_view(request):
    return render(request, "well_being/list.html",
                  {'well_being_list': ["Шаги"]})


def well_being_detail_view(request, well_being_type):
    interface = DbInterface()
    data = interface.fetch_steps_data()
    data.sort(key=lambda x: x[1])
    dates = [sublist[0] for sublist in data]
    steps = [sublist[1] for sublist in data]

    context = {
        'dates': dates,
        'steps': steps
    }

    return render(request, "well_being/detail.html", context)
