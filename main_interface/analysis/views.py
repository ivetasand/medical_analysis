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
    labs = [sublist[1] for sublist in obj]

    if obj[0][3]:
        results = [sublist[5] for sublist in obj]
        lower_limits = [sublist[7] for sublist in obj]
        upper_limits = [sublist[8] for sublist in obj]
        dates = [sublist[9] for sublist in obj]
        results_dates_lower_upper = zip(results, dates, lower_limits,
                                        upper_limits)
        months = __for_better_dates_display(dates)
        # results_dates_lower_upper_json = json.dumps(results_dates_lower_upper)

        context = {
            'analysis_type_name': obj[0][2],
            'units': obj[0][-1],
            'results_dates_lower_upper': results_dates_lower_upper,
            'results': results,
            'lower_limits': lower_limits,
            'upper_limits': upper_limits,
            'dates': dates,
            'months': months,
            'labs': labs
        }

        return render(request, "analysis/detail_numeric.html", context)

    else:
        results = [1 if sublist[4] == sublist[6] else 0 for sublist in obj]
        references = [sublist[6] for sublist in obj]
        dates = [sublist[9] for sublist in obj]
        months = __for_better_dates_display(dates)
        print(dates)
        context = {
            'analysis_type_name': obj[0][2],
            'results': results,
            'references': references,
            'dates': dates,
            'months': months,
            'labs': labs
        }
        return render(request, "analysis/detail_text.html", context)


def __for_better_dates_display(dates):
    months = []
    for date in dates:
        new_date = date[5:-3]
        match new_date:
            case '01':
                months.append(f"январь {date[:4]}")
            case '02':
                months.append(f"февраль {date[:4]}")
            case '03':
                months.append(f"март {date[:4]}")
            case '04':
                months.append(f"апрель {date[:4]}")
            case '05':
                months.append(f"май {date[:4]}")
            case '06':
                months.append(f"июнь {date[:4]}")
            case '07':
                months.append(f"июль {date[:4]}")
            case '08':
                months.append(f'август {date[:4]}')
            case '09':
                months.append(f"сентябрь {date[:4]}")
            case '10':
                months.append(f"октябрь {date[:4]}")
            case '11':
                months.append(f"ноябрь {date[:4]}")
            case '12':
                months.append(f"декабрь {date[:4]}")
    return months


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
            ["гемотест", "витамин А", 1, 0.8, 0.2, 0.8, "2023-06-14",
             "unit_name2"],
            ["гемотест", "витамин А", 1, 0.1, 0.2, 0.8, "2023-06-14",
             "unit_name2"],
            ["днком", "ВПЧ типы 51,56", 0, "обнаружено", "не обнаружено",
             "2023-01-27"],
            ["днком", "какой-то ещё анализ", 0, "обнаружено", "не обнаружено",
             "2023-05-27"],
            ["днком", "какой-то ещё анализ", 1, "обнаружено", "не обнаружено",
             "2023-05-30"]
        ]
    interface.insert_data(data_sample_for_testing)

    obj = interface.fetch_data()
    return render(request, "analysis/list.html", {'analysis_list': obj})
