from datetime import timedelta, date

from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Submit, Field
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from todolist.models import Problem, VALID_PROBLEM_TYPES, Subject, Homework
from todolist.util.parse_problem_url import parse_problem_url, InvalidURLDomain


def index(_):
    """
    Index page.  Just redirects to the problem list
    :param _: Request object
    :return:
    """
    # context = {}
    #
    # return render(req, 'todolist/index.html', context)
    return redirect('todolist:problems')


# OJ PROBLEMS

PROBLEM_TYPE_FIELD_CHOICES = (('auto', 'auto'),) + tuple(zip(VALID_PROBLEM_TYPES, VALID_PROBLEM_TYPES))


class ProblemForm(forms.Form):
    """
    Form for adding todo problems
    """
    link = forms.CharField(max_length=128, label='Link', widget=forms.TextInput(attrs={'size': 25}), required=True)
    name = forms.CharField(max_length=64, label='Name (generated if type is "auto")', required=False)
    type = forms.ChoiceField(choices=PROBLEM_TYPE_FIELD_CHOICES, initial='auto', label='Type:', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row('link'),
            Row('name'),
            Row('type'),
            Row(Submit('submit', 'Add'))
        )

    def clean(self):
        """
        Clean method override.  This override primarily deals with the "auto" type option
        :return:
        """

        cleaned_data = super().clean()

        if cleaned_data.get('type') == 'auto':
            problem_link = cleaned_data.get('link')
            try:
                problem_type, problem_name = parse_problem_url(problem_link)
                cleaned_data['type'] = problem_type
                cleaned_data['name'] = problem_name
            except InvalidURLDomain as e:
                if problem_link:
                    self.add_error('link', str(e))

        return cleaned_data


def problems(req):
    """
    Deals with requests to the "problems" path
    :param req: Request object
    :return:
    """

    form = ProblemForm(req.POST or None)

    if req.user.is_authenticated and form.is_valid():
        problem = Problem(**form.cleaned_data)
        problem.save()
        form = ProblemForm()
        messages.success(req, 'Added problem!')

    context = {'form': form,
               'problems': Problem.objects.order_by('type').order_by('link')}
    return render(req, 'todolist/problems.html', context)


@login_required(login_url='/login')
def remove_problem(req, problem_id):
    """
    Deals with requests to the "remove_problem" path
    :param req: Request object
    :param problem_id: Problem ID
    :return:
    """

    if req.user.is_authenticated:
        Problem.objects.filter(pk=problem_id).delete()
        messages.success(req, 'Removed problem!')
    else:
        messages.error(req, 'Insufficient permissions!')

    return redirect('todolist:problems')


# HOMEWORK

class SubjectForm(forms.Form):
    """
    Form for adding subjects
    """
    name = forms.CharField(max_length=64, label='Name', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row('name'),
            Row(Submit('submit', 'Add Subject'))
        )


ONE_DAY = timedelta(days=1)


def tommorow():
    """
    Tommorow's date
    :return: Tommorow's date
    """
    return date.today() + ONE_DAY


class HomeworkForm(forms.Form):
    name = forms.CharField(max_length=256, label='Name')
    subject = None
    due_date = forms.DateField(label='Due Date', required=True, initial=tommorow, widget=DatePickerInput())
    comments = forms.CharField(max_length=1024, label='Comments', widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices = [(subject.id, subject.name) for subject in Subject.objects.order_by('name').all()]
        self.fields['subject'] = forms.ChoiceField(
            choices=choices, label='Subject',
            required=True, widget=forms.Select(attrs={'size': len(choices)}))

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row('name'),
            Row('subject'),
            Row('due_date'),
            Row(Field('comments', rows='2', style='resize: none;')),
            Row(Submit('submit', 'Add Homework'))
        )

    def clean(self):
        """
        Validates "add homework" form.  Currently it just checks that the subject is valid and then sets it
        :return: Cleaned data
        """

        cleaned_data = super().clean()

        try:
            subject_id = int(cleaned_data.get('subject'))
            subject = Subject.objects.get(pk=subject_id)
            cleaned_data['subject'] = subject
        except TypeError:
            pass  # Assume the homework was not added using the proper form stuffs
        except ValueError:
            self.add_error('subject', 'Subject ID must be int!')
        except Subject.DoesNotExist:
            self.add_error('subject', f'Subject with id {subject_id} does not exist!')

        return cleaned_data


def homework(req):
    """
    Handles requests to the "homework" page
    :param req: The request
    :return:
    """

    homework_form = HomeworkForm()
    subject_form = SubjectForm()

    if req.user.is_authenticated:
        submit = req.POST.get('submit')
        if submit == 'Add Homework':
            homework_form = HomeworkForm(req.POST or None)
            if homework_form.is_valid():
                homework = Homework(**homework_form.cleaned_data)
                homework.save()
                messages.success(req, 'Added Homework!')
                homework_form = HomeworkForm()
        if submit == 'Add Subject':
            subject_form = SubjectForm(req.POST or None)
            if subject_form.is_valid():
                subject = Subject(**subject_form.cleaned_data)
                subject.save()
                messages.success(req, 'Added subject!')
                subject_form = SubjectForm()
                homework_form = HomeworkForm()  # Reload

    context = {'subject_form': subject_form, 'homework_form': homework_form,
               'subjects': Subject.objects.all().order_by('name'),
               'homeworks': Homework.objects.all().order_by('due_date')}
    return render(req, 'todolist/homework.html', context)


@login_required(login_url='login/')
def remove_subject(req, subject_id):
    """
    Handles requests for "removing subjects"
    :param req: Request object
    :param subject_id: The subject ID
    :return:
    """

    Subject.objects.filter(pk=subject_id).delete()
    messages.success(req, 'Removed subject!')
    return redirect('todolist:homework')


@login_required(login_url='login/')
def remove_homework(req, homework_id):
    """
    Handles requests for "removing homework"
    :param req: Request object
    :param homework_id: The homework ID
    :return:
    """

    Homework.objects.filter(pk=homework_id).delete()
    messages.success(req, 'Removed homework!')
    return redirect('todolist:homework')


def projects(req):
    context = {}

    return render(req, 'todolist/projects.html', context)
