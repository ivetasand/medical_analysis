from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from utils.database.interface import DbInterface
from .forms import TextForm, NumericForm


def analysis_detail_view(request, analysis_type):
    interface = DbInterface()

    obj = interface.fetch_analysis_data(analysis_type)
    labs = [sublist[1] for sublist in obj]

    if obj[0][3]:
        obj.sort(key=lambda x: x[9])

        results = [sublist[5] for sublist in obj if sublist[5] is not None]
        lower_limits = [sublist[7] for sublist in obj if sublist[5] is not None]
        upper_limits = [sublist[8] for sublist in obj if sublist[5] is not None]
        dates = [sublist[9] for sublist in obj if sublist[5] is not None]
        results_dates_lower_upper = zip(results, dates, lower_limits,
                                        upper_limits)
        months = __for_better_dates_display(dates)
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
        obj.sort(key=lambda x: x[9])

        results = [0 if sublist[4] == sublist[6] else 1 for sublist in obj]
        references = [sublist[6] for sublist in obj]
        dates = [sublist[9] for sublist in obj]
        months = __for_better_dates_display(dates)
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
    interface = DbInterface()
    obj = interface.fetch_analysis_data()
    obj.sort()
    return render(request, "analysis/list.html", {'analysis_list': obj})


def analysis_numeric_edit_view(request):
    if request.method == 'POST':
        form = NumericForm(request.POST)
        if form.is_valid():
            analysis_name = form.cleaned_data.get('analysis_name')
            lab_name = form.cleaned_data.get('lab_name')
            result_value = form.cleaned_data.get('result_value')
            lower_ref = form.cleaned_data.get('lower_ref')
            upper_ref = form.cleaned_data.get('upper_ref')
            timestamp = form.cleaned_data.get('timestamp')
            units = form.cleaned_data.get('units')
            db = DbInterface()
            db.insert_analysis_data([(lab_name, analysis_name, 1, result_value,
                                      lower_ref, upper_ref, timestamp, units)])
            return HttpResponseRedirect('http://127.0.0.1:7000/analysis_list/')
    else:
        form = NumericForm()

    context = {
        'form_key': form
    }
    return render(request, "analysis/edit/edit.html", context)


def analysis_text_edit_view(request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            analysis_name = form.cleaned_data.get('analysis_name')
            lab_name = form.cleaned_data.get('lab_name')
            result_text = form.cleaned_data.get('result_text')
            reference_text = form.cleaned_data.get('reference_text')
            timestamp = form.cleaned_data.get('timestamp')
            db = DbInterface()

            db.insert_analysis_data([(lab_name, analysis_name, 0, result_text,
                                      reference_text, timestamp)])
            return HttpResponseRedirect('http://127.0.0.1:7000/analysis_list/')
    else:
        form = TextForm()

    context = {
        'form_key': form
    }
    return render(request, "analysis/edit/edit.html", context)


def choice_view(request):
    if request.method == 'POST' and 'numeric_choice' in request.POST:
        return HttpResponseRedirect(
            'http://127.0.0.1:7000/analysis_edit/numeric/')
    elif request.method == 'POST' and 'text_choice' in request.POST:
        return HttpResponseRedirect(
            'http://127.0.0.1:7000/analysis_edit/text/')
    elif request.method == 'POST' and 'steps_choice' in request.POST:
        return HttpResponseRedirect(
            'http://127.0.0.1:7000/analysis_edit/steps/')
    elif request.method == 'POST' and 'delete_choice' in request.POST:
        db = DbInterface()
        db.delete_db()
        return HttpResponseRedirect('http://127.0.0.1:7000/home/')

    return render(request, "analysis/edit/choose.html", {})
