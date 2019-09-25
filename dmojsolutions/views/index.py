from crispy_forms.bootstrap import InlineField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from django import forms
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from dmojsolutions.models import Solution


class ProblemSearchForm(forms.Form):
    search = forms.CharField(max_length=40, initial='', label='Search Solutions: &nbsp;', required=False)
    offset = forms.IntegerField(initial=0, required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Row(
                'offset',
                Column('search', css_class='form-group'),

                InlineField(Submit('submit', 'Go')),
                Column(InlineField(Submit('submit', '<<'))),
                Column(InlineField(Submit('submit', '<'))),
                Column(InlineField(Submit('submit', '>')))
            )
        )


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
    form = ProblemSearchForm(req.GET or None)
    context = {'form': form}

    # Get Query Variables
    search = req.GET.get('search', '')
    try:
        offset_str = req.GET.get('offset', 0)
        offset = int(offset_str)
    except ValueError:
        messages.error(req, f'Invalid offset {offset_str}!')
        return redirect('dmojsolutions:index')

    # Get solution set
    qset = Solution.objects.only('problem').distinct().filter(
        Q(code__icontains=search) | Q(problem__name__icontains=search)).order_by('code')
    sols = qset[offset:offset + PROBLEMS_PER_PAGE]
    sol_cnt = sols.count()

    # Add solution set to context
    context['sols'] = sols

    # Set offsets
    context['offset'] = offset
    if offset - PROBLEMS_PER_PAGE >= 0:
        context['offset_prev'] = offset - PROBLEMS_PER_PAGE
    elif offset + PROBLEMS_PER_PAGE < sol_cnt:
        context['offset_next'] = offset + PROBLEMS_PER_PAGE

    # Set query
    context['cur_get_query'] = build_get_query({'search': search})

    return render(req, 'dmojsolutions/index.html', context)
