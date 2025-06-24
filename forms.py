from django import forms
from tasks.models import Task
#Django Form
class TaskForm(forms.Form):
    title=forms.CharField(max_length=250,label="Task Title")
    description=forms.CharField(widget=forms.Textarea,label="Task Description")
    due_date=forms.DateField(widget=forms.SelectDateWidget,label="Due Date")
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="Assign to Employees" )

    def __init__(self,*args, **kwargs):
        employees = kwargs.pop("employees", [])
        super().__init__(*args,**kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]
class StyleFormMixin(forms.Form):
    default_classes = 'border border-gray-300 rounded-lg w-full shadow-sm focus:border-rose-500 focus:ring-red-500'
    def apply_styled_widgets(self):
        for field in self.fields.values():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': self.default_classes, 'placeholder': f'Enter {field.label.lower()}'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': f"{self.default_classes} ", 'placeholder': f'Enter {field.label.lower()}', 'rows': 5})
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({'class': 'border border-gray-300 rounded-lg  shadow-sm focus:border-rose-500 focus:ring-red-500'})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': "space-y-2"})
                

 #Django Model Form
class TaskModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','description','due_date','assigned_to']
        widgets={
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple,
        }
    def __init__(self, *args, **kwargs):
        #employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs) 
        self.apply_styled_widgets()   
        # exclude=['project']
        # widgets = {
        #     'title':forms.TextInput(
        #         attrs={
        #                'class':'border border-gray-300 rounded-lg w-full shadow-sm focus:border-rose-500 focus:ring-red-500',
        #                'placeholder': 'Enter task title'}
        #         ),
        #         'description': forms.Textarea(
        #             attrs={
        #                'class':'border border-gray-300 rounded-lg w-full shadow-sm focus:border-rose-500 focus:ring-red-500',
        #                'placeholder': 'Enter task description',
        #                'rows': 5
        #                }
        #         ),
        #     'due_date': forms.SelectDateWidget(
        #         attrs={
        #                'class':'border border-gray-300 rounded-lg  shadow-sm focus:border-rose-500 focus:ring-red-500'
        #                }
        #     ),
        #     'assigned_to': forms.CheckboxSelectMultiple(),
        # }



        

