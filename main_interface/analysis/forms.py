from django import forms


class TextForm(forms.Form):
    lab_name = forms.CharField(label='Название лаборатории')
    analysis_name = forms.CharField(label='Название анализа')
    result_text = forms.CharField(label='Результат')
    reference_text = forms.CharField(label='Референсное значение')
    timestamp = forms.DateField(label='Дата сдачи')


class NumericForm(forms.Form):
    lab_name = forms.CharField(label='Название лаборатории')
    analysis_name = forms.CharField(label='Название анализа')
    result_value = forms.FloatField(label='Результат')
    lower_ref = forms.FloatField(label='Нижнее референсное')
    upper_ref = forms.FloatField(label='Верхнее референсное')
    timestamp = forms.DateField(label='Дата сдачи')
    units = forms.CharField(label='Единицы измерения')
