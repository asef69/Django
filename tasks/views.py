from django.db.models import Q,Count,Max,Min,Sum,Avg
from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm
from tasks.models import Employee, Task, Project
from datetime import date
from tasks.models import TaskDetails
from django.contrib import messages
# Create your views here.
def manager_dashboard(request):
    type = request.GET.get('type','all')
    tasks=Task.objects.select_related('details').prefetch_related('assigned_to').all()
    #Getting the total number of tasks
    # total_tasks = tasks.count()
    # completed_tasks = tasks.filter(status='COMPLETED').count()
    # in_progress_tasks = tasks.filter(status='IN_PROGRESS').count()
    # pending_tasks = tasks.filter(status='PENDING').count()
    # count={
    #     "total_tasks": tasks.count(),
    #     "completed_tasks": tasks.filter(status='COMPLETED').count(),
    #     "in_progress_tasks": tasks.filter(status='IN_PROGRESS').count(),
    #     "pending_tasks": tasks.filter(status='PENDING').count(),
    # }
    counts=Task.objects.aggregate(
        total_tasks=Count('id'),
        completed_tasks=Count('id', filter=Q(status='COMPLETED')),
        in_progress_tasks=Count('id', filter=Q(status='IN_PROGRESS')),
        pending_tasks=Count('id', filter=Q(status='PENDING')),

    )
    #Retriving tasks data
    base_query= Task.objects.select_related('details').prefetch_related('assigned_to')
    if type=="completed":
        tasks= base_query.filter(status='COMPLETED')
    elif type=="in_progress":
        tasks= base_query.filter(status='IN_PROGRESS')
    elif type=="pending":
        tasks= base_query.filter(status='PENDING')
    elif type=="all":
        tasks= base_query.all()        
    context={
        "tasks": tasks,
        "counts": counts,
    }
    return render(request,"dashboard/manager-dashboard.html",context)
def user_dashboard(request):
    return render(request,"dashboard/user-dashboard.html")
def test(request):
    context={
        "names":["John", "Jane", "Doe"],
        "age":[25, 30, 22],
        "city":["New York", "Los Angeles", "Chicago"],
    }
    return render(request,"test.html",context)
def create_task(request):
    task_form=TaskModelForm()
    task_detail_form=TaskDetailModelForm()
    if request.method == "POST": 
        task_form=TaskModelForm(request.POST)
        task_detail_form=TaskDetailModelForm(request.POST)
        form = TaskModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task created successfully!")
            return redirect('create_task')  # Redirect to the same page or another page after successful submission
        # else:
        #     # Return the form with errors
        #     return render(request, "task_form.html", {"form": form})
    
    # This is the important missing return for GET request
    context={
        "task_form": task_form,
        "task_detail_form": task_detail_form,
    }
    return render(request, "task_form.html", context)



def update_task(request,id):
    task=Task.objects.get(id=id)
    task_form=TaskModelForm(instance=task)
    if task.details: # type: ignore
        task_detail_form=TaskDetailModelForm(instance=task.details) # type: ignore
        
    if request.method == "POST": 
        task_form=TaskModelForm(request.POST,instance=task)
        task_detail_form=TaskDetailModelForm(request.POST,instance=task.details) # type: ignore
        form = TaskModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():
            task=task_form.save()

            task_detail=task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail_form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('update_task',id)  # Redirect to the same page or another page after successful submission
        # else:
        #     # Return the form with errors
        #     return render(request, "task_form.html", {"form": form})
    
    # This is the important missing return for GET request
    context={
        "task_form": task_form,
        "task_detail_form": task_detail_form, # type: ignore
    }
    return render(request, "task_form.html", context)

def view_task(request):
    #rendering all the data form the tasks model
    # tasks=Task.objects.all()
    # task_3=Task.objects.get(id=3)
    # first_task=Task.objects.first()
    #tasks=Task.objects.filter(due_date=date.today())
    #tasks=TaskDetails.objects.exclude(priority='L').select_related('task')
    #tasks=Task.objects.filter(title__icontains="paper")
    #tasks=Task.objects.filter(Q(status='PENDING') | Q(status='IN_PROGRESS'))
    #tasks=TaskDetails.objects.select_related('task').all()
    #tasks=Task.objects.select_related('project').all()
    #tasks= Task.objects.prefetch_related('assigned_to').all()
    projects=Project.objects.annotate(
        num_tasks=Count('task'),
        
    ).order_by('name')
    return render(request, "show_task.html", {"tasks": projects})
def delete_task(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('manager_dashboard')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('manager_dashboard')
