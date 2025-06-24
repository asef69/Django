from django.urls import path
from tasks.views import manager_dashboard,user_dashboard,test,create_task
urlpatterns = [
    path('manager-dashboard/', manager_dashboard),
    path('user-dashboard/', user_dashboard),  
    path('test/',test),
    path('create_task/',create_task)# Assuming user_dashboard uses the same view for simplicity
]

