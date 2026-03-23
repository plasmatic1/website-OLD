import json
from urllib import request
from urllib.error import URLError

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import redirect

from dmojsolutions.models import Problem, Solution
from view_utils import superuser_required
from .github_util import codes_for_ext


def get_json(url):
    with request.urlopen(url) as resp:
        return json.loads(resp.read())


PROBLEMS_LIST_URL = 'https://dmoj.ca/api/v2/problems'


@superuser_required(url_pattern_name='dmojsolutions:index')
@login_required(login_url='login')
def reload_problems(req):
    try:
        new_problems = get_json(PROBLEMS_LIST_URL)
        total_pages = new_problems['data']['total_pages']

        messages.add_message(req, messages.INFO, 'Found %d pages of problems!' % total_pages)

        problems = []
        for page in range(1, total_pages + 1):
            if page == 1:
                page_problems = new_problems
            else:
                page_problems = get_json(f'{PROBLEMS_LIST_URL}?page={page}')

            for obj in page_problems['data']['objects']:
                problems.append(Problem(code=obj['code'], name=obj['name'], group=obj['group']))

            messages.add_message(req, messages.INFO, 'Loaded %d problems from page %d!' % (len(page_problems['data']['objects']), page))

        if not problems:
            raise ValueError('Problem API returned no objects.')

        with transaction.atomic():
            Problem.objects.all().delete()
            Problem.objects.bulk_create(problems)

        messages.add_message(req, messages.INFO, 'Added %d problems!' % len(problems))
    except URLError as e:
        if hasattr(e, 'code'):
            msg = 'Error %s: %s' % (e.code, e.reason)
        else:
            msg = '%s' % e.reason
        messages.add_message(req, messages.WARNING, msg)
    except (KeyError, TypeError, ValueError) as e:
        messages.add_message(req, messages.WARNING, f'Problem import failed: {e}')

    return redirect('dmojsolutions:index')


@superuser_required(url_pattern_name='dmojsolutions:index')
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

    return redirect('dmojsolutions:index')


@superuser_required(url_pattern_name='dmojsolutions:index')
@login_required(login_url='login')
def delete_problems(req):
    Problem.objects.all().delete()
    messages.add_message(req, messages.INFO, 'Success!')

    return redirect('dmojsolutions:index')


@superuser_required(url_pattern_name='dmojsolutions:index')
@login_required(login_url='login')
def delete_solutions(req):
    Solution.objects.all().delete()
    messages.add_message(req, messages.INFO, 'Success!')

    return redirect('dmojsolutions:index')
