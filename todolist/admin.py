from django.contrib import admin
from .models import *


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'name',)
    list_filter = ('user',)
    search_fields = ('user', 'name',)
    ordering = ('user', 'name',)


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'name', 'due_date', 'comments')
    list_filter = ('user', 'subject',)
    search_fields = ('user', 'subject', 'name')
    ordering = ('user', 'subject', 'due_date', 'name')


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('user', 'link', 'name', 'type')
    list_filter = ('user', 'type',)
    search_fields = ('user', 'link', 'name', 'type')
    ordering = ('user', 'link', 'name')

    def name(self, obj):
        return 'N/A' if len(obj.name) == 0 else obj.name


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description')
    list_filter = ('user',)
    search_fields = ('user', 'name',)
    ordering = ('user', 'name',)

    def description(self, obj):
        return obj.description if len(obj.description) < 30 else obj.description[:30] + '...'


# Register your models here.
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Project, ProjectAdmin)
