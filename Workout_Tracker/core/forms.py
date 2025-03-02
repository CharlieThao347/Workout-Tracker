from django import forms
from django.core import validators
from django.contrib.auth.models import User
from core.models import Exercise, Workout, ExerciseDetails

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')
        help_texts = {
            'username': None
        }

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'style':'max-width: 15em'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style':'max-width: 15em'}))

class WorkoutForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput())

class ExerciseForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput())
    class Meta():
        model = Exercise
        fields = ("name",)

class ExerciseDetailsForm(forms.ModelForm):
    reps = forms.IntegerField(widget=forms.TextInput(),validators=[validators.MinValueValidator(0)])
    sets = forms.IntegerField(widget=forms.TextInput(),validators=[validators.MinValueValidator(0)])
    weight = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'123','style':'font-size:medium'}),validators=[validators.MinValueValidator(0)])
    class Meta():
        model = ExerciseDetails
        fields = ("sets", "reps", "weight",)
