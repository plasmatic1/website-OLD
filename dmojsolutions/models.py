from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Create your models here.
from dmojsolutions.views.github_util import src_for_code


class Problem(models.Model):
    code = models.CharField(max_length=32, verbose_name='Problem Code')
    name = models.CharField(max_length=256, verbose_name='Problem Name')
    group = models.CharField(max_length=64, verbose_name='Group')

    def solution(self, ext):
        try:
            return Solution.objects.get(ext=ext, code=self.code)
        except ObjectDoesNotExist:
            return None

    @property
    def cpp_solution(self):
        return self.solution('cpp')

    @property
    def py_solution(self):
        return self.solution('py')

    @property
    def has_solution(self):
        return self.cpp_solution or self.py_solution

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class Solution(models.Model):
    code = models.CharField(max_length=32, verbose_name='Problem Code')
    ext = models.CharField(max_length=16, verbose_name='File Extension')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)

    @property
    def src(self):
        return src_for_code(self.ext, '%s.%s' % (self.code, self.ext))
