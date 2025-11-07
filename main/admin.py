from django.contrib import admin
from .models import Project, ContactMessage
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title','created_at')
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name','email','created_at')
