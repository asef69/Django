from django.urls import path
from tasks.views import show_task,show_specific_task
urlpatterns = [
    path("show_tasks/",show_task),
    path('show_tasks/<id>/',show_specific_task)
]
