import json
from urllib import request
from urllib.error import URLError

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from app.models import Problem, Solution

from .github_util import codes_for_ext


def get_json(url):
    with request.urlopen(url) as resp:
        return json.loads(resp.read())


PROBLEMS_LIST_URL = 'https://dmoj.ca/api/problem/list'


@login_required(login_url='login')
def reload_problems(req):
    try:
        new_problems = get_json(PROBLEMS_LIST_URL)

        Problem.objects.all().delete()
        problems = []
        for k, obj in new_problems.items():
            problems.append(Problem(code=k, name=obj['name'], group=obj['group']))
        Problem.objects.bulk_create(problems)

        messages.add_message(req, messages.INFO, 'Added %d problems!' % len(problems))
    except URLError as e:
        if hasattr(e, 'code'):
            msg = 'Error %s: %s' % (e.code, e.reason)
        else:
            msg = '%s' % e.reason

        messages.add_message(req, messages.WARNING, msg)

    return redirect('index')


@login_required(login_url='login')
def delete_problems(req):
    Problem.objects.all().delete()
    messages.add_message(req, messages.INFO, 'Success!')

    return redirect('index')


@login_required(login_url='login')
def reload_solutions(req):
    Solution.objects.all().delete()
    solutions = []
    for file in codes_for_ext('cpp') + codes_for_ext('py'):
        code, ext, *ot = file.split('.')

        if len(ot):
            continue

        try:
            problem = Problem.objects.get(code=code)
        except ObjectDoesNotExist:
            problem = None

        solutions.append(Solution(code=code, ext=ext, problem=problem))
    Solution.objects.bulk_create(solutions)

    messages.add_message(req, messages.INFO, 'Added %d solutions!' % len(solutions))

    return redirect('index')


@login_required(login_url='login')
def delete_solutions(req):
    Solution.objects.all().delete()
    messages.add_message(req, messages.INFO, 'Success!')

    return redirect('index')
