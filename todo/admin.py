from django.contrib import admin
from .models import Todo

class ReadFiels(admin.ModelAdmin):
  readonly_fields = ('creation_date',)


admin.site.register(Todo, ReadFiels)