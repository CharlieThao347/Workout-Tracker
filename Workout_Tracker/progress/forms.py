from django import forms
from progress.models import Exercise, ExerciseCategory, Weight
from django.core import validators

class ExerciseForm(forms.ModelForm):
    exercise = forms.ModelChoiceField(queryset=ExerciseCategory.objects.all())
    class Meta():
        model = Exercise
        fields = ('exercise',)
class WeightForm(forms.ModelForm):
    weight = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'123','style':'font-size:medium'}),validators=[validators.MinValueValidator(0)])
    class Meta():
        model = Weight
        fields = ('weight',)
