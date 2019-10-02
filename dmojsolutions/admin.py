from django.contrib import admin
from .models import *


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'group')
    list_filter = ('group',)
    search_fields = ('code', 'name')
    ordering = ('code',)


class SolutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'ext', 'group')
    list_filter = ('problem__group', 'ext')
    search_fields = ('problem__name', 'problem__group', 'code')
    ordering = ('code',)

    def name(self, obj):
        return 'N/A (%s)' % obj.code if obj.problem is None else obj.problem.name

    def group(self, obj):
        return 'N/A' if obj.problem is None else obj.problem.group


# Register your models here.
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Solution, SolutionAdmin)
