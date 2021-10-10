from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from todo.forms import TodoForm
from todo.models import Todo

# Create your views here.


def home(request):
    return render(request, "todo/home.html")


def signupuser(request):
    if request.method == "GET":
        context = {"form": UserCreationForm()}
        return render(request, "todo/signupuser.html", context)

    elif request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"]
                )
                user.save()
                login(request, user)
                return redirect("currenttodos")

            except (IntegrityError, ValueError):
                context = {
                    "form": UserCreationForm(),
                    "error": "username already been taken",
                }
                return render(request, "todo/signupuser.html", context)
        else:
            context = {"form": UserCreationForm(), "error": "Password did not match"}
            return render(request, "todo/signupuser.html", context)


def loginuser(request):
    if request.method == "GET":
        return render(request, "todo/login.html")
    else:
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        print(request.POST.get("username"))
        if user is None:
            context = {
                "form": AuthenticationForm(),
                "error": "This username is not registered.",
            }
            return render(request, "todo/login.html", context)
        else:
            login(request, user)
            return redirect("currenttodos")


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")


@login_required
def currenttodos(request):
    user_todos = Todo.objects.filter(owner=request.user, conclusion_date__isnull=True)
    return render(request, "todo/currenttodos.html", {"todos": user_todos})


@login_required
def viewtodo(request, todo_pk):
    todo_item = get_object_or_404(Todo, id=todo_pk, owner=request.user)
    if request.method == "GET":
        form = TodoForm(instance=todo_item)
        return render(
            request, "todo/viewtodo.html", {"todo_item": todo_item, "form": form}
        )
    elif request.method == "POST":
        try:
            form = TodoForm(request.POST, instance=todo_item)
            form.save()
            return redirect("currenttodos")
        except ValueError:
            return render(
                request,
                "todo/viewtodo.html",
                {"todo_item": todo_item, "form": form, "error": "Bad data"},
            )


@login_required
def createtodo(request):
    if request.method == "GET":
        return render(request, "todo/createtodo.html", {"form": TodoForm()})
    else:
        form = TodoForm(request.POST)
        new_todo = form.save(commit=False)
        new_todo.owner = request.user
        new_todo.save()
        return redirect("currenttodos")


@login_required
def completetodo(request, todo_pk):
    todo_item = get_object_or_404(Todo, id=todo_pk, owner=request.user)
    if request.method == "POST":
        todo_item.conclusion_date = timezone.now()
        todo_item.save()
        return redirect("currenttodos")


@login_required
def deletetodo(request, todo_pk):
    todo_item = get_object_or_404(Todo, id=todo_pk, owner=request.user)
    if request.method == "POST":
        todo_item.delete()
        return redirect("currenttodos")


@login_required
def completedtodos(request):
    user_todos = Todo.objects.filter(owner=request.user, conclusion_date__isnull=False)
    return render(request, "todo/currenttodos.html", {"todos": user_todos})
