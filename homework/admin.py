from django.contrib import admin

from .models import Homework
# Register your models here.

class HomeworkAdmin(admin.ModelAdmin):
    pass

admin.site.register(Homework, HomeworkAdmin)
