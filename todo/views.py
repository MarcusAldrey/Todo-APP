from todo.models import Todo
from todo.forms import TodoForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
  return render(request,'todo/home.html')


def signupuser(request):
  
  if request.method == 'GET':
    return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
  
  elif request.method == 'POST':
    if request.POST['password1'] == request.POST['password2']:
      try:
        user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
        user.save()
        login(request, user)
        return redirect('currenttodos')

      except (IntegrityError, ValueError):
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':"username already been taken"})
    else:
      return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':"Password did not match"})

@login_required
def loginuser(request):
  if request.method == 'GET':
    return render(request, 'todo/login.html', {'form':AuthenticationForm()})
  else:
    user = authenticate(request, username=request.POST['username'], password=request.POST['password']) 
    if user is None:
      return render(request, 'todo/login.html', {'form':AuthenticationForm(), 'error':'Erro ao logar'})
    else:
      login(request, user)
      return redirect('currenttodos')

def logoutuser(request):
  if request.method == 'POST':
    logout(request)
    return redirect('home')

@login_required
def currenttodos(request):
  user_todos = Todo.objects.filter(owner=request.user, conclusion_date__isnull=True)
  return render(request, 'todo/currenttodos.html',{'todos':user_todos})

@login_required
def viewtodo(request, todo_pk):
  todo_item = get_object_or_404(Todo,id=todo_pk, owner=request.user)
  if (request.method == 'GET'):
    form = TodoForm(instance=todo_item)
    return render(request, 'todo/viewtodo.html',{'todo_item':todo_item,'form':form})
  elif (request.method == 'POST'):
    try:  
      form = TodoForm(request.POST, instance=todo_item)
      form.save()
      return redirect('currenttodos')
    except ValueError:
      return render(request, 'todo/viewtodo.html', {'todo_item':todo_item,'form':form, 'error':"Bad data"})



  


@login_required
def createtodo(request):
  if request.method == 'GET':
    return render(request, 'todo/createtodo.html',{'form':TodoForm()})
  else:
    form = TodoForm(request.POST)
    new_todo = form.save(commit=False)
    new_todo.owner = request.user
    new_todo.save()
    return redirect('currenttodos')

@login_required
def completetodo(request,todo_pk):
  todo_item = get_object_or_404(Todo,id=todo_pk, owner=request.user)
  if (request.method == 'POST'):
    todo_item.conclusion_date = timezone.now()
    todo_item.save()
    return redirect('currenttodos')

@login_required
def deletetodo(request,todo_pk):
  todo_item = get_object_or_404(Todo,id=todo_pk, owner=request.user)
  if (request.method == 'POST'):
    todo_item.delete()
    return redirect('currenttodos')

@login_required
def completedtodos(request):
  user_todos = Todo.objects.filter(owner=request.user, conclusion_date__isnull=False)
  return render(request, 'todo/currenttodos.html',{'todos':user_todos})