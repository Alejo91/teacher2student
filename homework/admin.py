from django.contrib import admin

from .models import Homework, Answer
# Register your models here.

class HomeworkAdmin(admin.ModelAdmin):
    pass

class AnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Answer, AnswerAdmin)
