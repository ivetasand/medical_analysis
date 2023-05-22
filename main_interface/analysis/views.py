from django.shortcuts import render
from django.http import HttpResponse
from utils.database.interface import DbInterface
import json


# Create your views here.
def analysis_detail_view(request, analysis_type):
    # Эта штука должна создаваться вообще где-то в одном месте, не?
    # for testing
    interface = DbInterface()

    # пока будем брать нулевой
    obj = interface.fetch_data(analysis_type)

    if obj[0][3]:
        results = [sublist[5] for sublist in obj]
        lower_limits = [sublist[7] for sublist in obj]
        upper_limits = [sublist[8] for sublist in obj]
        dates = [sublist[9] for sublist in obj]
        results_dates_lower_upper = zip(results, dates, lower_limits,
                                        upper_limits)
        # results_dates_lower_upper_json = json.dumps(results_dates_lower_upper)

        context = {
            'analysis_type_name': obj[0][2],
            'units': obj[0][-1],
            'results_dates_lower_upper': results_dates_lower_upper,
            'results': results,
            'lower_limits': lower_limits,
            'upper_limits': upper_limits,
            'dates': dates
        }

        return render(request, "analysis/detail_numeric.html", context)

    else:
        results = [sublist[4] for sublist in obj]
        references = [sublist[6] for sublist in obj]
        dates = [sublist[9] for sublist in obj]

        context = {
            'analysis_type_name': obj[0][2],
            'results': results,
            'references': references,
            'dates': dates
        }
        return render(request, "analysis/detail_text.html", context)


def analysis_list_view(request):
    # for testing
    interface = DbInterface()

    data_sample_for_testing = \
        [
            # [lab_name, analysis_type_name, is_result_numeric, result_text,
            # reference_text, date]
            ["днком", "ВПЧ типы 51,56", 0, "не обнаружено", "не обнаружено",
             "2022-01-27"],
            # [lab_name, analysis_type_name, is_result_numeric, result_value,
            # reference_lower_value,reference_upper_value, date, units]
            ["гемотест", "витамин А", 1, 0.5, 0.2, 0.8, "2023-05-14",
             "unit_name2"],
            ["гемотест", "витамин А", 1, 0.6, 0.2, 0.8, "2023-06-14",
             "unit_name2"],
            ["днком", "ВПЧ типы 51,56", 0, "обнаружено", "не обнаружено",
             "2023-01-27"],
            ["днком", "какой-то ещё анализ", 0, "обнаружено", "не обнаружено",
             "2023-05-27"]
        ]
    interface.insert_data(data_sample_for_testing)

    obj = interface.fetch_data()
    return render(request, "analysis/list.html", {'analysis_list': obj})
