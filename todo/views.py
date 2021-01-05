from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone


def home(request):
    return render(request, 'todo/home.html')


def signupUser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupUser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentTodos')
            except IntegrityError:
                return render(request, 'todo/signupUser.html',
                              {'form': UserCreationForm(), 'error': 'Username already taken. Please choose another username..'})
        else:
            return render(request, 'todo/signupUser.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match.'})


def loginUser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginUser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginUser.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('currentTodos')


@login_required
def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def createTodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createTodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currentTodos')
        except ValueError:
            return render(request, 'todo/createTodo.html', {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})


@login_required
def currentTodos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'todo/currentTodos.html', {'todos': todos})


@login_required
def completedTodos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'todo/completedTodos.html', {'todos': todos})


@login_required
def viewTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewTodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currentTodos')
        except ValueError:
            return render(request, 'todo/viewTodo.html', {'todo': todo, 'error': 'Bad info.'})


@login_required
def completeTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('currentTodos')


@login_required
def deleteTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        if todo.date_completed:
            todo.delete()
            return redirect('completedTodos')
        else:
            todo.delete()
            return redirect('currentTodos')