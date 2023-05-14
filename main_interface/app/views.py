from django.http import Http404
from django.shortcuts import render, get_object_or_404
# from .models import Analysis, AnalysisResult
from datetime import datetime, timedelta
from django.db.models import Avg
from django.db.models.functions import TruncDay
from django.shortcuts import render, redirect
from .forms import MyLoginForm


def index_view(request):
    # Получаем список всех доступных анализов
    # analysis_list = Analysis.objects.all()
    analysis_list = ["analysis1",'analysis2']
    # Определяем анализ, выбранный пользователем по умолчанию
    default_analysis = analysis_list.first()

    # Получаем результаты анализов для выбранного анализа
    # results = AnalysisResult.objects.filter(analysis=default_analysis)
    results = analysis_list
    # Определяем даты и значения для графика
    dates = [result.date for result in results]
    values = [result.value for result in results]
    
    # Получаем нижнее и верхнее значение нормы анализа
   # lower_norm = default_analysis.lower_norm
   # upper_norm = default_analysis.upper_norm

    # Передаем данные в шаблон и отображаем его
    context = {
        'analysis_list': analysis_list,
        'selected_analysis': default_analysis,
        'dates': dates,
        'values': values,
        #'lower_norm': lower_norm,
        #'upper_norm': upper_norm,
    }
    return render(request, 'analysis/index.html', context)

def analysis_list(request):
    # analysis_list = Analysis.objects.all()
    analysis_list = ["analysis1", 'analysis2']
    return render(request, 'analysis_list.html', {'analysis_list': analysis_list})


def analysis_detail(request, analysis_id):
    # try:
    #     analysis = Analysis.objects.get(pk=analysis_id)
    # except Analysis.DoesNotExist:
    #     raise Http404("Анализ не найден")

    # results = AnalysisResult.objects.filter(analysis=analysis).order_by('date')
    analysis = ['']
    results = ['']
    context = {
        'analysis': analysis,
        'results': results,
    }

    return render(request, 'analysis_detail.html', context)


def home(request):
    # analyses = Analysis.objects.all()
    analyses = ["analysis1", 'analysis2']
    context = {'analyses': analyses}
    return render(request, 'home.html', context)


def plot_view(request, analysis_id):
    # Получаем анализ, выбранный пользователем
    # Получаем результаты анализов для выбранного анализа
    # необходимо заменить на единый select через бек.
    # selected_analysis = Analysis.objects.get(id=analysis_id)
    # results = AnalysisResult.objects.filter(analysis=selected_analysis)
    selected_analysis = ['']
    results = ['']

    # Определяем даты и значения для графика
    dates = [result.date for result in results]
    values = [result.value for result in results]

    # Получаем нижнее и верхнее значение нормы анализа
    lower_norm = selected_analysis.lower_norm
    upper_norm = selected_analysis.upper_norm

    # Передаем данные в шаблон и отображаем его
    context = {
        'analysis_list': ["analysis1"], #Analysis.objects.all(),
        'selected_analysis': selected_analysis,
        'dates': dates,
        'values': values,
        'lower_norm': lower_norm,
        'upper_norm': upper_norm,
    }
    return render(request, 'analysis/index.html', context)

def charts(request):
    # Получаем выбранный анализ из POST-запроса
    selected_analysis_id = request.POST.get('analysis_id')

    # Получаем список всех доступных анализов
    # не нужно вроде
    # analysis_list = Analysis.objects.all()

    # Получаем результаты анализов для выбранного анализа
    results = ['']
    #results = AnalysisResult.objects.filter(analysis=selected_analysis_id)

    # Определяем даты и значения для графика
    dates = [result.date for result in results]
    values = [result.value for result in results]


    # Вычисляем средние значения анализов за каждый день
    daily_averages = results.annotate(date_day=TruncDay('date'))\
                             .values('date_day')\
                             .annotate(average=Avg('value'))\
                             .order_by('date_day')

    # Получаем значения верхней и нижней нормы для данного типа анализа
    upper_norm = 100
    lower_norm = 50

    # Выводим результаты на страницу
    return render(request, 'charts.html', {'selected_analysis': selected_analysis_id,
                                            'daily_averages': daily_averages,
                                            'upper_norm': upper_norm,
                                            'lower_norm': lower_norm})



# def login_view(request):
#     if request.method == 'POST':
#         form = MyLoginForm(request.POST)
#         if form.is_valid():
#             login = form.cleaned_data['login']
#             password = form.cleaned_data['password']
#             select = form.cleaned_data['select']
#             # Do something with the parameters
#             if select == 'option2':
#                 print(gemotest("93079180", "79267039809"))
#     else:
#         form = MyLoginForm()
#     return render(request, 'login.html', {'form': form})
