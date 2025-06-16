from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to the Task Management System!")
def contact(request):
    return HttpResponse("<h1 style='color:red'>This is the Contact page.</h1>")
def show_task(request):
    return HttpResponse("<h1 style='color:blue'>This is the  Task page.</h1>")
def show_specific_task(request,id):
    print("id ",id)
    print("id type ",type(id))
    return HttpResponse("This is our specific task menu")
