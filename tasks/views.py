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
    employees=Employee.objects.all()
    form=TaskModelForm()
    if request.method=="POST":
        form=TaskForm(request.POST,employees=employees)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            due_date = form.cleaned_data.get('due_date')
            assigned_to = form.cleaned_data.get('assigned_to')
            task=Task.objects.create(
                title=title,
                description=description,
                due_date=due_date,
            )
            for id in assigned_to:
                employee=Employee.objects.get(id=id)
                task.assigned_to.add(employee)
            return HttpResponse("Task created successfully!")    
    context={
        "form":form
    }
    return render(request,"task_form.html",context)