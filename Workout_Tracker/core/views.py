from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from core.models import Workout, Exercise, ExerciseDetails
from core.forms import JoinForm, LoginForm, WorkoutForm, ExerciseForm, ExerciseDetailsForm
from django.contrib.auth.models import User

@login_required(login_url='/login/')
def home(request):
    msg = ""
    if (Workout.objects.filter(user=request.user, completed=False).count() == 0):
        msg = "You currently have no workouts"
        return render(request, 'core/home.html', context={"msg": msg})
    elif (request.method == "GET" and "delete" in request.GET):
        id = request.GET["delete"]
        Workout.objects.filter(id=id).delete()
        return redirect("/")
    else:
        table_data = Workout.objects.filter(user=request.user, completed=False)
        context = {
        "table_data": table_data
        }
        return render(request, 'core/home.html', context)

@login_required(login_url='/login/')
def add(request):
    if (request.method == "POST"):
        if ("add" in request.POST):
            workout_form = WorkoutForm(request.POST)
            if (workout_form.is_valid()):
                name = workout_form.cleaned_data["name"]
                user = User.objects.get(id=request.user.id)
                Workout(user=user, name=name).save()
                return redirect("/")
            else:
                context = {
                "workout_form": workout_form
                }
                return render(request, 'core/add.html', context)
        else:
            return redirect("/")
    else:
        context = {
        "workout_form": WorkoutForm()
        }
        return render(request, 'core/add.html', context)

@login_required(login_url='/login/')
def complete(request, id):
	if (request.method == "GET"):
		workout = Workout.objects.get(id=id)
		workout.completed = True
		workout.save()
		return redirect("/")
	elif (request.method == "POST"):
		return redirect("/")

@login_required(login_url='/login/')
def view(request, id):
    if (request.method == "GET" and "delete" in request.GET):
        previous_page = request.POST.get('previous_page')
        workout = Workout.objects.get(id=id)
        id = request.GET["delete"]
        exercise = Exercise.objects.get(id=id)
        workout.exercises.remove(exercise)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        workout = Workout.objects.get(id=id)
        table_data = ExerciseDetails.objects.filter(workout=workout)
        msg = ""
        if (workout.exercises.count() == 0):
            msg = "There are no exercises for this workout"
        id = id
        context = {
        "table_data": table_data,
        "id": id,
        "msg": msg
        }
        return render(request, 'core/view.html', context)

@login_required(login_url='/login/')
def add_exercise(request, id):
    id = id
    url = "/core/view/" + str(id) + "/"
    if (request.method == "POST"):
        if ("add_exercise" in request.POST):
            exercise_form = ExerciseForm(request.POST)
            exercise_details_form = ExerciseDetailsForm(request.POST)
            if (exercise_form.is_valid() and exercise_details_form.is_valid()):
                name = exercise_form.cleaned_data["name"]
                exercise = Exercise.objects.create(name=name)
                reps = exercise_details_form.cleaned_data["reps"]
                sets = exercise_details_form.cleaned_data["sets"]
                weight = exercise_details_form.cleaned_data["weight"]
                ExerciseDetails.objects.create(workout=Workout.objects.get(id=id), exercise=exercise, reps=reps, sets=sets, weight=weight)
                return redirect(url)
            else:
                context = {
                "exercise_form": exercise_form,
                "exercise_details_form": exercise_details_form,
                "id": id
                }
                return render(request, 'core/add_exercise.html', context)
        else:
            return redirect(url)
    else:
        context = {
        "exercise_form": ExerciseForm(),
        "exercise_details_form": ExerciseDetailsForm(),
        "id": id
        }
        return render(request, 'core/add_exercise.html', context)

@login_required(login_url='/login/')
def edit_exercise(request, id, num):
    id = id
    url = "/core/view/" + str(id) + "/"
    if (request.method == "GET"):
        exercise_instance = Exercise.objects.get(id=num)
        exercise_form = ExerciseForm(instance=exercise_instance)
        exercise = ExerciseDetails.objects.get(exercise=exercise_instance)
        exercise_details_form = ExerciseDetailsForm(instance=exercise)
        context = {"exercise_form": exercise_form,
                    "exercise_details_form": exercise_details_form,
                    "id": id}
        return render(request, 'core/edit_exercise.html', context)
    elif (request.method == "POST"):
        if ("edit_exercise" in request.POST):
            exercise_form = ExerciseForm(request.POST)
            exercise_details_form = ExerciseDetailsForm(request.POST)
            if (exercise_form.is_valid() and exercise_details_form.is_valid()):
                name = exercise_form.cleaned_data["name"]
                exercise = Exercise.objects.get(id=num)
                exercise.name  = name
                exercise.save()
                reps = exercise_details_form.cleaned_data["reps"]
                sets = exercise_details_form.cleaned_data["sets"]
                weight = exercise_details_form.cleaned_data["weight"]
                ED = ExerciseDetails.objects.get(workout=Workout.objects.get(id=id), exercise=exercise)
                ED.sets = sets
                ED.reps = reps
                ED.weight = weight
                ED.save()
                return redirect(url)
            else:
                context= {
                "exercise_form": exercise_form,
                "exercise_details_form": exercise_details_form,
                "id": id
                }
                return render(request, 'core/edit_exercise.html', context)
        else:
            return redirect(url)

@login_required(login_url='/login/')
def completed_workouts(request):
    msg = ""
    if (Workout.objects.filter(user=request.user, completed=True).count() == 0):
        msg = "You have not completed any workouts"
        return render(request, 'core/completed_workouts.html', context={"msg": msg})
    elif (request.method == "GET" and "delete" in request.GET):
        id = request.GET["delete"]
        Workout.objects.filter(id=id).delete()
        return redirect("/core/completed_workouts/")
    elif (request.method == "GET" and "delete_all" in request.GET):
        Workout.objects.filter(user=request.user, completed=True).all().delete()
        return redirect("/core/completed_workouts/")
    else:
        table_data = Workout.objects.filter(user=request.user, completed=True)
        context = {
        "table_data": table_data
        }
        return render(request, 'core/completed_workouts.html', context)

@login_required(login_url='/login/')
def completed_view(request, id):
        workout = Workout.objects.get(id=id)
        table_data = ExerciseDetails.objects.filter(workout=workout)
        id = id
        context = {
        "table_data": table_data,
        "id": id,
        }
        return render(request, 'core/completed_view.html', context)

def about(request):
    return render(request, 'core/about.html')

def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            user = join_form.save()
            user.set_password(user.password)
            user.save()
            return redirect("/")
        else:
            page_data = { "join_form": join_form }
            return render(request, 'core/join.html', page_data)
    else:
        join_form = JoinForm()
        page_data = { "join_form": join_form }
        return render(request, 'core/join.html', page_data)

def user_login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect("/")
                else:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return render(request, 'core/login.html', {"login_form": LoginForm})
    else:
        return render(request, 'core/login.html', {"login_form": LoginForm})

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect("/")
