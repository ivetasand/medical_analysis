from django import forms


class StepsForm(forms.Form):
    steps_count = forms.FloatField(label='Количество шагов')
    timestamp = forms.DateField(label='Дата')
