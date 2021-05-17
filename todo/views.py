from todo.models import Todo
from todo.forms import TodoForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

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

      except IntegrityError:
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':"username already been taken"})
    else:
      return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':"Password did not match"})

def currenttodos(request):
  user_todos = Todo.objects.filter(owner=request.user, conclusion_date__isnull=True)
  return render(request, 'todo/currenttodos.html',{'todos':user_todos})

def logoutuser(request):
  if request.method == 'POST':
    logout(request)
    return redirect('home')
  
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

def createtodo(request):
  if request.method == 'GET':
    return render(request, 'todo/createtodo.html',{'form':TodoForm()})
  else:
    form = TodoForm(request.POST)
    new_todo = form.save(commit=False)
    new_todo.owner = request.user
    new_todo.save()
    return redirect('currenttodos')