from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from dmojsolutions.models import Solution, Problem
from dmojsolutions.views.github_util import rate_limit


class SolutionSearchForm(forms.Form):
    """
    Form for solution searching
    """
    search = forms.CharField(max_length=40, initial='', label='Search:', required=False)
    offset = forms.IntegerField(initial=0, required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'get'
        # self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Row(
                Column(Submit('submit', '<<', css_class='btn-sm', css_id='offset-first')),
                Column(Submit('submit', '<', css_class='btn-sm', css_id='offset-prev')),
                Column(Submit('submit', '>', css_class='btn-sm', css_id='offset-next')),
                css_class='mt-1'
            ),
            Row(
                'offset',
                Column('search', css_class='form-group'),
            ),
            Row(
                Submit('submit', 'Go')
            )
        )

        # Make form data mutable
        self.data = self.data.copy()


PROBLEMS_PER_PAGE = 30


def build_get_query(req_get):
    """
    Builds a url query (for GET requests) using the supplied req_get object
    :param req_get: The req.GET property of the request object passed to django view functions
    :return: The url query
    """

    if req_get:
        return '&'.join([f'{k}={v}' for k, v in req_get.items()]) + ''
    else:
        return ''


def index(req):
    form = SolutionSearchForm(req.GET or None)
    context = {'form': form, 'rate_limit': rate_limit}  # Context fields that can be determined at the start

    # Get Query Variables
    search = req.GET.get('search', '')
    try:
        offset_str = req.GET.get('offset', 0)
        offset = int(offset_str)
    except ValueError:
        messages.error(req, f'Invalid offset {offset_str}!')
        return redirect('dmojsolutions:index')

    # Get solution set
    qset = Solution.objects.distinct().filter(
        Q(code__icontains=search) | Q(problem__name__icontains=search)).filter(problem__isnull=False).order_by('code')
    sol_cnt = qset.count()

    # Changed offset based on submit button clicked
    submit = req.GET.get('submit', 'Go')
    if submit == '<<':
        offset = 0
    elif submit == '<':
        if offset - PROBLEMS_PER_PAGE > 0:
            offset -= PROBLEMS_PER_PAGE
        else:
            messages.error(req, 'Invalid offset for submit method! (<)')
    elif submit == '>':
        if offset + PROBLEMS_PER_PAGE < sol_cnt:
            offset += PROBLEMS_PER_PAGE
        else:
            messages.error(req, 'Invalid offset for submit method! (>)')
    elif submit != 'Go':
        messages.error(req, 'Invalid submit method!')

    # Get solution set and add to context
    sols = [x.problem for x in qset[offset:offset + PROBLEMS_PER_PAGE]]
    context['solution_count'] = sol_cnt
    context['solutions'] = sols

    # Set offsets
    context['offset'] = offset
    context['offset_next'] = min(sol_cnt - 1, offset + PROBLEMS_PER_PAGE - 1)
    context['offset_can_go_back'] = int(offset > 0)
    context['offset_can_go_forward'] = int(offset + PROBLEMS_PER_PAGE < sol_cnt)
    form.data['offset'] = offset  # Set offset on form

    # Set query
    context['cur_get_query'] = build_get_query({'search': search})

    return render(req, 'dmojsolutions/index.html', context)


PDF_URL_FORMAT = 'https://dmoj.ca/problem/%s/pdf'


def view(req, code, lang):
    solution = get_object_or_404(Solution, ext=lang, code=code)
    problem = get_object_or_404(Problem, id=solution.problem_id)

    context = {'code': code, 'ext': lang, 'problem': problem, 'pdf_link': PDF_URL_FORMAT % code,
               'src': solution.src, 'user': req.user}

    return render(req, 'dmojsolutions/view.html', context)


def raw(req, code, lang):
    solution = get_object_or_404(Solution, ext=lang, code=code)
    return render(req, 'dmojsolutions/raw.html', {'ext': lang, 'code': code, 'src': solution.src})
