from django.db import models

# Create your models here.
class Employee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    def __str__(self):
        return self.name
    

class Project(models.Model):
    name=models.CharField(max_length=100)
    start_date=models.DateField()
    description=models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed'),
        # ('ON_HOLD','On Hold'),
        # ('CANCELLED','Cancelled'),
    ]
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks',null=True,blank=True)
    #notun_string=models.CharField(max_length=100,default="")
    title=models.CharField(max_length=250)
    assigned_to = models.ManyToManyField(Employee, default=1,related_name="tasks")
    description=models.TextField()
    due_date=models.DateField()
    status=models.CharField(max_length=15,choices=STATUS_CHOICES,default='PENDING')
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class TaskDetails(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS=(
        (HIGH,'High'),
        (MEDIUM,'Medium'),
        (LOW,'Low'),
    )
    #std_id=models.CharField(max_length=200,primary_key=True)
    task=models.OneToOneField(Task,on_delete=models.CASCADE,related_name='details')
    #assigned_to = models.CharField(max_length=100)
    priority=models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default=LOW)
    notes=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Details for {self.task.title} "


