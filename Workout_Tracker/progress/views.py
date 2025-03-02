from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from progress.models import Exercise, ExerciseCategory, Weight
from progress.forms import ExerciseForm, WeightForm
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='/login/')
def progress(request):
    if (ExerciseCategory.objects.count() == 0):
        list = ["Bench Press", "Squat", "Deadlift", "Shoulder Press", "Barbell Curl", "Bent Over Row", "Sled Leg Press"]
        for exercise in list:
            ExerciseCategory(exercises=exercise).save()
    if (request.method == "GET" and "delete" in request.GET):
        Exercise.objects.filter(user=request.user).delete()
        Weight.objects.filter(user=request.user).all().delete()
        return redirect("/progress/")
    else:
        msg = ""
        if (Exercise.objects.filter(user=request.user).count() == 0):
            msg = "You are not currently tracking progress for any exercise."
            return render(request, 'progress/progress.html', context={"msg": msg})
        exercise_weight = []
        for each in Weight.objects.filter(user=request.user).all():
            exercise_weight.append(each.weight)
        exercise_name = Exercise.objects.get(user=request.user).exercise_name
        context = {
        "msg" : msg,
        "exercise_name": exercise_name,
        "exercise_weight": exercise_weight,
        }
        return render(request, 'progress/progress.html', context)

@login_required(login_url='/login/')
def add(request):
    if (request.method == "POST"):
        if ("add" in request.POST):
            exercise_form = ExerciseForm(request.POST)
            weight_form = WeightForm(request.POST)
            if (exercise_form.is_valid() and weight_form.is_valid()):
                exercise = exercise_form.cleaned_data["exercise"]
                weight = weight_form.cleaned_data["weight"]
                user = User.objects.get(id=request.user.id)
                Exercise(user=user, exercise_name=exercise).save()
                Weight(user=user, weight=weight).save()
                return redirect("/progress/")
            else:
                context = {
                "exercise_data": exercise_form,
                "weight_data": weight_form
                }
                return render(request, 'progress/add.html', context)
        else:
            return redirect("/progress/")
    else:
        context = {
        "exercise_data": ExerciseForm(),
        "weight_data": WeightForm()
        }
        return render(request, 'progress/add.html', context)

@login_required(login_url='/login/')
def add_entry(request):
    exercise_name = Exercise.objects.get(user=request.user).exercise_name
    if (request.method == "POST"):
        if ("add_entry" in request.POST):
            weight_form = WeightForm(request.POST)
            if (weight_form.is_valid()):
                weight = weight_form.cleaned_data["weight"]
                user = User.objects.get(id=request.user.id)
                Weight(user=user, weight=weight).save()
                return redirect("/progress/")
            else:
                context = {
                "weight_data": weight_form,
                "exercise_name": exercise_name
                }
                return render(request, 'progress/add_entry.html', context)
        else:
            return redirect("/progress/")
    else:
        context = {
        "weight_data": WeightForm(),
        "exercise_name": exercise_name
        }
        return render(request, 'progress/add_entry.html', context)
