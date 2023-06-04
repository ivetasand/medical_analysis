from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import StepsForm
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

def steps_edit_view(request):

    if request.method == 'POST':
        form = StepsForm(request.POST)
        if form.is_valid():
            steps_count = form.cleaned_data.get('steps_count')
            timestamp = form.cleaned_data.get('timestamp')
            db = DbInterface()

            db.insert_steps_data([[timestamp, steps_count]])
            return HttpResponseRedirect('http://127.0.0.1:7000/well_being/')
    else:
        form = StepsForm()

    context = {
        'form_key': form
    }

    return render(request, "well_being/edit/steps.html", context)