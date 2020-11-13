from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import TaskList
from .forms import TaskForm

# Create your views here.
@login_required
def todoList(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request, ("New Task Added."))
        return redirect('todoList')
    else:
        all_tasks = TaskList.objects.filter(manage=request.user)

        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('pg')

        all_tasks = paginator.get_page(page)

        context = {}
        context["welcomeText"]= "Welcome ToDo List Page"
        context["all_tasks"]= all_tasks
        return render(request, 'todoList.html', context)

@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request, ("Access Restricted! You are not allowed...."))
    return redirect('todoList')

@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, ("Access Restricted! You are not allowed...."))
    return redirect('todoList')
    
@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = False
        task.save()
    else:
        messages.error(request, ("Access Restricted! You are not allowed...."))
    return redirect('todoList')

@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
        messages.success(request, ("Task Edited."))
        return redirect('todoList')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        context = {}
        context["welcomeText"]= "Welcome Update Page"
        context["task_obj"]= task_obj
        return render(request, 'edit.html', context)

def index(request):
    context = {}
    context["welcomeText"]= "Welcome Home Page"
    return render(request, 'index.html', context)

def contact(request):
    context = {}
    context["welcomeText"]= "Welcome Contact Page"
    return render(request, 'contact.html', context)

def about(request):
    context = {}
    context["welcomeText"]= "Welcome About Page"
    return render(request, 'about.html', context)