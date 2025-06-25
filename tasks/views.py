from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee, Task
# Create your views here.
def manager_dashboard(request):
    return render(request,"dashboard/manager-dashboard.html")
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
    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "task_form.html", {
                "form": TaskModelForm(),  # reset form after success
                "message": "Task created successfully!"
            })
        else:
            # Return the form with errors
            return render(request, "task_form.html", {"form": form})
    
    # This is the important missing return for GET request
    form = TaskModelForm()
    return render(request, "task_form.html", {"form": form})
def view_task(request):
    #rendering all the data form the tasks model
    tasks=Task.objects.all()
    task_3=Task.objects.get(id=3)
    first_task=Task.objects.first()
    return render(request, "show_task.html", {"tasks": tasks, "task_3": task_3, "first_task": first_task})


