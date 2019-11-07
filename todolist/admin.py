from django.contrib import admin
from .models import *


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'due_date', 'comments')
    list_filter = ('subject',)
    search_fields = ('subject', 'name')
    ordering = ('subject', 'due_date', 'name')


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('link', 'name', 'type')
    list_filter = ('type',)
    search_fields = ('link', 'name', 'type')
    ordering = ('link', 'name')

    def name(self, obj):
        return 'N/A' if len(obj.name) == 0 else obj.name


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

    def description(self, obj):
        return obj.description if len(obj.description) < 30 else obj.description[:30] + '...'


# Register your models here.
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Project, ProjectAdmin)
