from django import forms
from .models import Category, Task

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'color': forms.TextInput(attrs={'placeholder': 'Color', 'type':'color'}),
            'icon': forms.TextInput(attrs={'placeholder': 'Ícono (Material Design)'}),
        }
        fields = ('name', 'color', 'icon')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'título'}),
            'date': forms.TextInput(attrs={'placeholder': 'título', 'type':'datetime-local', 'required':'True'}),
            'description': forms.Textarea(attrs={'placeholder': 'título', 'rows':"3", 'placeholder':"Descripción"}),
        }
        fields = ('title', 'category', 'date', 'description')