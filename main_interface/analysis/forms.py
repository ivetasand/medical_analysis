from django import forms


class TextForm(forms.Form):
    analysis_name = forms.CharField()


class NumericForm(forms.Form):
    analysis_name = forms.CharField()


class ChooseAnalysisType(forms.Form):
    choice = ('numeric', 'text')
    type = forms.ChoiceField(choices=choice)
