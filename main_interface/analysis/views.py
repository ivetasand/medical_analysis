from django.shortcuts import render
from django.http import HttpResponse
from utils.database.interface import DbInterface


# Create your views here.
def analysis_detail_view(request, analysis_type):
    # analysis_type = "витамин А"

    # Эта штука должна создаваться вообще где-то в одном месте, не?
    # for testing
    interface = DbInterface()
    data_sample_for_testing = \
        [
            ["днком", "ВПЧ типы 51,56", 0, "не обнаружено",
             0, "не обнаружено", "2022-01-27", "unit_name1"],
            ["гемотест", "витамин А", 1, 0.5, 1, 0.2, 0.8, "2023-05-14",
             "unit_name2"]
        ]
    # interface.insert_data(data_sample_for_testing)

    # пока будем брать нулевой
    obj = interface.fetch_data(analysis_type)[0]
    print(obj)
    # 2, 'гемотест', 'витамин А', 1, None, 0.5, 1, None, 0.2, 0.8, '2023-05-14', 'unit_name2'
    context = {
        'lab_name': obj[1],
        'analysis_name': obj[2],
    }
    print(context)
    return render(request, "analysis/detail.html", context)


def analysis_list_view(request):
    # for testing
    interface = DbInterface()
    obj = interface.fetch_data()
    return render(request, "analysis/list.html", {'analysis_list': obj})
