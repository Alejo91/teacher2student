from django.contrib import admin
from .models import SchoolUser
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(SchoolUser, UserAdmin)
