from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from todo.forms import TodoForm
from todo.models import Todo


def home(request):
    return render(request, "todo/home.html")


def signupuser(request):
    if request.method == "GET":
        return render(request, "todo/signupuser.html")

    elif request.method == "POST":
        if request.POST["password"] == request.POST["passwordconfirmation"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"],
                    password=request.POST["password"],
                    email=request.POST["email"],
                )
                if User.objects.filter(email=request.POST["email"]).exists():
                    context = {"error": "Email already been registered"}
                    return render(request, "todo/signupuser.html", context)
                user.save()
                login(request, user)
                return redirect("currenttodos")

            except (IntegrityError, ValueError):
                context = {"error": "Username already been taken"}
                return render(request, "todo/signupuser.html", context)
        else:
            context = {"error": "Password did not match"}
            return render(request, "todo/signupuser.html", context)


def loginuser(request):
    if request.method == "GET":
        return render(request, "todo/login.html")
    elif request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user is None:
            context = {"error": "This username is not registered"}
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
        return render(request, "todo/viewtodo.html", {"todo_item": todo_item})
    elif request.method == "POST":
        try:
            todo_item.title = request.POST["title"]
            todo_item.memo = request.POST["memo"]
            print(request.POST.get("memo"))
            todo_item.important = (
                True if request.POST.get("important") == "true" else False
            )
            todo_item.save()
            return redirect("currenttodos")
        except ValueError:
            return render(
                request,
                "todo/viewtodo.html",
                {"todo_item": todo_item, "error": "Bad data"},
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
