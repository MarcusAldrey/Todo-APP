from django.forms import ModelForm, fields
from .models import Todo

class TodoForm(ModelForm):
  class Meta:
    model = Todo
    fields = ['title', 'memo', 'important']